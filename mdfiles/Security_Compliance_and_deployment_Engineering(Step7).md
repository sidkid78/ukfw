## **1. Security Architecture Overview**

### **Backend (FastAPI):**

- **Authentication**: Azure Active Directory (AAD) OAuth2/JWT integration (enterprise SSO & token validation for all endpoints)
- **Authorization**: Role-Based Access Control (RBAC) mapped via Azure AD Groups & graph-level roles
- **API Access**: Secure HTTPs (TLS, e.g. Azure Application Gateway), automatic OpenAPI endpoint restrictions
- **Audit Trails**: Every API mutating call is metadata/audit-enriched (user, timestamp, action)
- **Node Compliance Visibility**: Run-time enforcement using axis8 ("compliance" axis) across all data reads/writes
- **Metadata Tagging**: Compliance tags (HIPAA, GDPR, etc) and provenance/versioning on all nodes/pillars
- **Regulatory Auditability**: Endpoints and logs for audit extraction (who/what/when/how revealed)
- **Monitoring & Telemetry**: Azure Monitor + Application Insights integrated (PII-redacted logs/events)
- **Pipeline Security**: Azure DevOps “Build & Release”, policies for approval, secret scanning, artifact integrity, and IaC (Bicep/Terraform for infrastructure)
- **Edge/Air-gapped/Cloud Support**: Deployable as a container (Docker), in-model with local AAD or fallback local-only RBAC mode

### **Frontend (Next.js):**

- **AAD User Login**: NextAuth.js (or MSAL.js) with SSO
- **Role/Compliance-Aware UI**: Frontend disables/hides any node/axis forbidden by compliance flag or user role
- **Secure API Calls**: JWT bearer tokens passed to backend for every API request, errors handled gracefully
- **Audit UX**: Display provenance, version, compliance, audit trails visibly where appropriate

---

## **2. Detailed Implementation Steps**

### **2.1 Azure Active Directory Authentication (FastAPI backend)**

- **Register App in Azure AD:**
    - Register a new Application (App Registration)
    - Configure redirect URIs for dev/prod
    - Obtain `client_id`, `tenant_id`, `client_secret`
    - Set API permissions (openid, profile, email, etc), assign groups
- **Token Validation Middleware:**
    - Use [fastapi-azure-auth](https://github.com/Azure/fastapi-azure-auth) or [authlib](https://docs.authlib.org/en/latest/client/fastapi.html#fastapi) to enforce authentication

**Example (`security.py`):**

```python
from fastapi import Depends, HTTPException, status, Security
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer, GraphGroup
from fastapi.security import OAuth2PasswordBearer

# Setup AAD OIDC
azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id='<your-client-id>',
    tenant_id='<your-tenant-id>',
    openapi_authorization_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    openapi_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    scopes={"api://<your-app-id>/user_impersonation": "User Impersonation"},
)

def require_authenticated_user(user=Security(azure_scheme)):
    # Optionally, inject user claims here for downstream use
    return user

def require_role(required_group_id: str):
    def inner(user=Security(azure_scheme)):
        if required_group_id not in user.group_ids:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return inner

```

**Usage in API Endpoints (`api.py`):**

```python
from security import require_authenticated_user, require_role

@router.get("/nodes/{node_id}", dependencies=[Depends(require_authenticated_user)])
def get_node(...):
    ...

@router.post("/nodes/", dependencies=[Depends(require_role(SUPERUSER_GROUP_ID))])
def create_node(...):
    ...

```

- Map RBAC group IDs to compliance roles (“compliance reader”, “editor”, etc).
- Make user info available in request context for audit, metadata, logging.

---

### **2.2 Compliance Tag Enforcement (Backend Layer)**

- Every node/pillar has `axis8` (compliance flags, e.g. `['GDPR', 'HIPAA']`)
- On every data read or query, backend cross-references user compliance claims (fetched from JWT or from Azure AD custom claims) with node requirements:
    - If non-intersecting, **403 Forbidden**

**In Endpoint—Example:**

```python
# In api.py, extended:
@router.get("/nodes/{node_id}")
def get_node(node_id: str, user=Depends(require_authenticated_user)):
    node = kgm.get_node_by_id(node_id)
    user_compliance = user.claims.get('compliance', [])
    # Already filtered in compliance.py, but double-check per user context!
    if node.axes.axis8 and not any(tag in user_compliance for tag in (node.axes.axis8 if isinstance(node.axes.axis8, list) else [node.axes.axis8])):
        raise HTTPException(status_code=403, detail="Restricted by compliance policy")
    ...

```

---

### **2.3 Secure Metadata & Audit Logging**

- Every write/mutate (create, update, simulation refine, confidence update) attaches an audit record:
    - Who (`user_id`/`aad_oid`)
    - What (operation, before/after)
    - When (timestamp, ISO 8601 UTC)
    - From where (IP, app)
    - Compliance context (what tags, roles)
    - Optional: Raw JWT or event signature

**In Model:**

```python
# When creation/update
def log_audit_event(action, node, user, extra=None):
    audit = {
        'user_id': user.oid,
        'user_email': user.email,
        'action': action,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'compliance_context': node.axes.axis8,
        'client_ip': user.client_ip or 'unknown',
        **(extra or {}),
    }
    node.metadata.setdefault('audit_trail', []).append(audit)

```

- On request: `/nodes/{node_id}?audit=true` can return audit history if the user is in an “auditor” AAD group.

---

### **2.4 Monitoring, Alerting, and Telemetry**

- **Azure Application Insights / Monitor:**
    - All logs, errors, request traces, PII-redacted
    - Custom events: compliance breach attempts, unauthorized access, simulation activities
- **Health Endpoint:** `/healthz` shallow probe (secured if sensitive)

**Usage (in `main.py`):**

```python
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=<your-key>'))
# Use logger.info, logger.error etc throughout app

```

---

### **2.5 CI/CD & Infrastructure Security**

- **Repo/Code Security (DevSecOps):**
    - Branch protection, code reviews, SAST scanning (SonarQube, GitHub Advanced Security)
    - No secrets in code; use Azure Key Vault for all secrets (AAD client, API keys, etc.)
- **Azure Pipelines/Terraform/Bicep for deployment:**
    - Infrastructure-as-Code: App Service, AKS or Container Instances, App Gateway
    - Deploy with MSI (Managed Service Identities) where possible, not service principals w/secrets
    - Only allow AAD-authenticated pipeline service account to deploy
    - Use `az login --identity` for managed identity deployments
    - CI runs auto-tests, lint, security checks, builds container with provenance
    - CD requires RBAC approval for production push (auditable)
    - Harden container (non-root user, resource limits, auto-updates off, no SSH/extra ports)
- **Edge Support:** Build images with all dependencies, configs can fallback to “local” RBAC if no AAD; sign images (cosign/sbom)

---

### **2.6 Frontend Security & Compliance**

- **Next.js App Router (Edge/Server/Client components):**
    - Use [NextAuth.js](https://next-auth.js.org/) or MSAL.js for Azure AD login—users only see UI after login
    - Fetch tokens with `acquireTokenSilent`, attach `Bearer` in `Authorization` header for API calls; refresh on expiration
    - Map user AAD group/claims to UI roles: compliance reader, editor, auditor
    - **UI Filtering**: All compliance-bound info (nodes, badges, panels) must first check compliance/visibility returned from backend before rendering; never trust client-only suppression
    - **No sensitive info** is rendered in HTML or stored in browser storage
    - **Front-end errors** for attempted access to forbidden content (user sees “Insufficient Compliance/Privilege”)
        - Do not leak existence/ID of forbidden resources
- **Audit UX:** Expose audit/provenance panels only to auditor/editor roles (read from user claims).

---

### **2.7 Regulatory & Compliance Controls**

### **HIPAA/GDPR/IEEE 7000:**

- **GDPR Data Subject Access:** API endpoint (with strict RBAC) to export all user data (“right to be forgotten” in audit-trail, etc)
- **HIPAA:** All PHI fields (if any, e.g., in simulated medical pillar) are tagged in axis8, available only to “HIPAA-cleared” group
- **ISO/IEEE:** System & software engineering evidence, capability, and audit documentation exportable as JSON for compliance review.
- **Metadata for Compliance:** Each node/pillar must have metadata: `axis8` (tags), `provenance` (source), `version`, `review_history` (who, when, what changed), and (optionally) encryption at rest.

### **Compliance Pipeline Checks:**

- Build policy: Fail builds on missing compliance tags or metadata in any new node/pillar YAMLs (test script)
- Static analysis scans YAML/data for accidental PII or forbidden terms

---

### **2.8 Deployment Patterns**

- **Cloud Native (Azure):**
    - **AKS (Kubernetes)**: For scalable, HA backend/api; RBAC via Azure AD
    - **App Service (Web App for Containers)**: For smaller installs
    - **Application Gateway**: TLS termination, WAF
    - **Private Link/NAT Gateway**: No public endpoints if needed
    - **Key Vault**: Holds API secrets, connection strings
    - **Azure AD Groups**: Assign global RBAC/compliance
- **Edge / In-Model Deployments:**
    - Omit cloud AAD and storage as needed
    - Use local YAML+RBAC configuration
    - All compliance/audit logic remains functional; audit logs are written to local file or syslog for later export
- **Deployment Automation:** Bicep/Terraform IaC module examples:

```
resource webapp 'Microsoft.Web/sites@2023-01-01' = {
  // ...
  identity: { type: 'SystemAssigned' }
  appSettings: [
    { name: 'AAD_CLIENT_ID', value: aadApp.applicationId }
    { name: 'KEYVAULT_URL', value: keyVault.properties.vaultUri }
    // ...
  ]
}

```

---

### **2.9 Role/Compliance Model Example**

| **AAD Role/Group** | **API Permissions** | **UI/Graph Permissions** |
| --- | --- | --- |
| `ukfw_user` | Read visible nodes/pillars | Browse, explore |
| `ukfw_editor` | Read/write where allowed | Edit/create nodes (if permitted) |
| `ukfw_compliance` | See compliance/GDPR/PHI nodes | Access sensitive tags |
| `ukfw_auditor` | All audit logs, panel access | Export audit, provenance view |

---

## **3. Example Workflow**

1. **User Logs In via Azure AD** (OIDC / NextAuth), SSO across UI and API
2. **Backend Enforces Authentication & RBAC**:
    - JWT validated
    - User roles/groups extracted
    - All node/pillar access is filtered by compliance tags in axis8 and user compliance claims
    - All creation/update endpoints check role/groups
3. **Frontend Loads Only Allowed Content**:
    - UI disables/hides content the API didn’t return
    - Compliance/audit/provenance indicators visible only if user’s group allows
4. **All Actions/Critical Reads are Audited**:
    - Backend logs action, user, timestamp, compliance context in node metadata
    - Azure Monitor streams PII-stripped logs for security ops
5. **Regulatory/Audit Export**:
    - GDPR/HIPAA/IEEE compliance data/Audit trails exportable via secured endpoint, to authorized groups only

---

## **4. SUMMARY TABLE**

| **Engineering Domain** | **Measures Implemented** | **Key Details** |
| --- | --- | --- |
| Authn/Authz | Azure AD SSO, JWT, RBAC | All endpoints, fine-grained, SSO across stack |
| Compliance | axis8 enforcement, metadata tagging | Node-level, in queries, creation, UI, pipeline |
| Auditability | Per-action audit trail, exportable logs | Linked in metadata, export on demand |
| Monitoring | Azure App Insights, `logging` integration | Secure log streaming, error/alerting |
| CI/CD | Azure DevOps, Key Vault, IaC pipelines, secret mgmt | No hardcoded secrets, signed reproducible builds |
| Cloud Deploy | AKS/AppService, AppGateway, PrivateLink, managed ident | Everything RBAC/AAD secured, edge fallback ready |
| Edge/Air-gapped | In-model fallback, local RBAC, local logs | Supports all compliance logic even offline |
| Frontend Security | NextAuth/MSAL, bearer tokens, UI filtering | Compliance UX, never trust client-only suppression |
| Regulatory Compliance | GDPR/HIPAA/IEEE, metadata, audit, DSAR export points | Pre-delivered, tested, surfaced via API |

---

## **5. Concrete Next Steps / Checklist**

- [ ]  **AAD Registration**: Setup and configure service principals + RBAC groups
- [ ]  **FastAPI Security Layer**: Implement token validation, RBAC decorators, inject audit metadata
- [ ]  **Compliance Logic**: Axis8 check in read/write path, enforce everywhere
- [ ]  **Audit Metadata**: Stamp on all mutating operations, expose via endpoint for auditor group
- [ ]  **Strict DevSecOps**: No secrets/leaks, PR security enforcement, build attestation
- [ ]  **Monitor/Alert**: Wire logs to Azure Monitor, setup dashboards/alerts (compliance breach, 403 floods)
- [ ]  **Frontend SSO Setup**: Integrate NextAuth/MSAL.js, propagate token to API, enforce UI role filtering
- [ ]  **Regulatory Test**: Simulate “right to be forgotten/gone”, “PHI access”, “audit export” test flows
- [ ]  **Infra-as-Code**: Write Bicep/Terraform templates for repeatable, reviewable deployment

---

## **6. Reference Stack**

- **Backend**: FastAPI, [fastapi-azure-auth](https://github.com/Azure/fastapi-azure-auth), PyYAML, Azure Monitor
- **Frontend**: Next.js App Router, [NextAuth.js](https://next-auth.js.org/) or [MSAL.js](https://github.com/AzureAD/microsoft-authentication-library-for-js), TypeScript
- **DevOps**: Azure DevOps, GitHub Actions, SonarQube
- **Deployment**: AKS/App Service, App Gateway, Key Vault, Private Link, edge container option
- **Compliance**: Metadata in YAML, runtime in axis8, API + pipeline checks

---

## **7. Final Notes**

This security & compliance architecture delivers **enterprise-grade, production-proven defense-in-depth** and auditability without impeding UKFW's advanced in-memory/simulation flows or multi-modal/edge potential.

- **All dynamic access is policy-driven (AAD+compliance+RBAC)**, audit trails are native and regulatory exports are attainable.
- **Design is modular**: swappable for non-Azure cloud, or fallback to local-only modes for isolated deployments.

---

### **You are now ready to hand off this specification to platform/infra engineers, security/compliance officers, or use as the base for regulatory review and operational rollout.**