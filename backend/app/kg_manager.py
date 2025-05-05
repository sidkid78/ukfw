import yaml
from typing import List, Optional, Dict
# Import all models needed
from .models import (
    KnowledgeNode, Pillar, # Keep old ones temporarily if needed elsewhere?
    Regulation, Provision, Role, Expert,
    SpiderwebNode, HoneycombNode, OctopusNode, RegulatoryAxis
)

class KnowledgeGraphManager:
    def __init__(self, 
                 regulations_path: str, 
                 provisions_path: str, 
                 roles_path: str, # Add roles path
                 experts_path: str, # Add experts path
                 mappings_path: Optional[str] = None):
        # Updated storage for specific types
        self.regulations: Dict[str, Regulation] = {}
        self.provisions: Dict[str, Provision] = {}
        self.roles: Dict[str, Role] = {}
        self.experts: Dict[str, Expert] = {}
        self.spiderwebs: Dict[str, SpiderwebNode] = {}
        self.honeycombs: Dict[str, HoneycombNode] = {}
        self.octopuses: Dict[str, OctopusNode] = {}
        # Consider a compliance status store if needed
        self.compliance_status: Dict[str, Dict] = {} # {provision_id: {"status": float, "value": float}}
        
        # Load all data sources
        self.load_regulations(regulations_path)
        self.load_roles(roles_path) # Load roles before provisions that might reference them
        self.load_experts(experts_path) # Load experts before provisions
        self.load_provisions_and_others(provisions_path) # Now load provisions
        if mappings_path:
            self.load_mappings(mappings_path)
            
        # Link roles/experts back to provisions
        self._link_entities()

    def load_regulations(self, file_path: str):
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                loaded_count = 0
                skipped_count = 0
                for item in data.get('pillars', []): 
                    item_id = item.get('id')
                    # Skip items without a valid ID
                    if not item_id or not isinstance(item_id, str):
                        print(f"Warning: Skipping regulation entry due to missing/invalid ID: {item}")
                        skipped_count += 1
                        continue
                        
                    # Map fields from Pillar structure to Regulation model
                    try:
                        reg = Regulation(
                            id=item_id,
                            title=item.get('name', 'Unnamed Regulation'), 
                            description=item.get('description'), # Correct field name
                            # Assuming a field like 'domain' or 'category' maps to 'pillar'
                            # !! Adjust 'item.get(...)' key if your YAML uses a different field name for pillar
                            pillar=item.get('pillar') or item.get('domain') or item.get('category', 'Unknown Pillar'), 
                            jurisdiction=item.get('jurisdiction', 'Universal'), 
                            location_code=item.get('location_code'), # Add mapping if available
                            effective_date=item.get('effective_date'), # Add mapping if available
                            provisions=[] # Initialize empty provisions list
                        )
                        self.regulations[reg.id] = reg
                        loaded_count += 1
                    except Exception as validation_error:
                        print(f"Warning: Skipping regulation entry ID '{item_id}' due to validation error: {validation_error}")
                        skipped_count += 1
                        
                print(f"Regulations loaded: {loaded_count}, skipped: {skipped_count}")
        except FileNotFoundError:
            print(f"Warning: Regulations file (expecting pillars) not found at {file_path}")
        except Exception as e:
            print(f"Error loading regulations (from pillars) from {file_path}: {e}")
            
    def load_roles(self, file_path: str):
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                for item in data.get('roles', []):
                    # Ensure provisions list is initialized if not present in YAML
                    item['provisions'] = item.get('provisions', []) 
                    role = Role(**item)
                    if role.id:
                        self.roles[role.id] = role
        except FileNotFoundError:
            print(f"Warning: Roles file not found at {file_path}")
        except Exception as e:
            print(f"Error loading roles from {file_path}: {e}")

    def load_experts(self, file_path: str):
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                for item in data.get('experts', []):
                     # Ensure provisions list is initialized if not present in YAML
                    item['provisions'] = item.get('provisions', [])
                    expert = Expert(**item)
                    if expert.id:
                        self.experts[expert.id] = expert
        except FileNotFoundError:
            print(f"Warning: Experts file not found at {file_path}")
        except Exception as e:
            print(f"Error loading experts from {file_path}: {e}")
            
    def load_provisions_and_others(self, file_path: str):
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                for item in data.get('nodes', []): 
                    axes = item.get('axes', {})
                    metadata = item.get('metadata', {})
                    
                    axis7_val = axes.get('axis7')
                    axis8_val = axes.get('axis8')
                    axis13_dict = axes.get('axis13', {})
                    tags_val = axis13_dict.get('tags') if isinstance(axis13_dict, dict) else axis13_dict
                    # Extract potential roles from axis12
                    axis12_val = axes.get('axis12')
                    potential_roles = [axis12_val] if isinstance(axis12_val, str) else (axis12_val if isinstance(axis12_val, list) else [])
                    # !! IMPORTANT: Need a way to map role NAMES from axis12 (e.g., "Theoretical Physicist") 
                    # to actual Role IDs (e.g., "ROLE_TP") loaded from roles.yaml.
                    # For now, we store the names from axis12 but this needs refinement.
                    # Ideally, nodes.yaml would use Role IDs directly in axis12.
                    roles_responsible_names = potential_roles # Store names for now

                    octopus_refs = [axis7_val] if isinstance(axis7_val, str) else (axis7_val if isinstance(axis7_val, list) else [])
                    crosswalks = [axis8_val] if isinstance(axis8_val, str) else (axis8_val if isinstance(axis8_val, list) else [])
                    tags = [tags_val] if isinstance(tags_val, str) else (tags_val if isinstance(tags_val, list) else [])

                    prov = Provision(
                        id=item.get('node_id'), 
                        regulation_id=item.get('pillar_id'), 
                        title=item.get('label', 'Untitled Provision'), 
                        text=item.get('description', ''), 
                        section=axes.get('axis3'),
                        parent_id=item.get('parent_id'),
                        jurisdiction=item.get('jurisdiction', self.regulations.get(item.get('pillar_id')).jurisdiction if item.get('pillar_id') in self.regulations else 'Universal'),
                        hierarchy_level=axes.get('axis4'),
                        octopus_refs=octopus_refs, 
                        crosswalks=crosswalks, 
                        tags=tags,
                        # Store the names for now - TODO: map names to IDs
                        roles_responsible=roles_responsible_names, 
                        spiderweb_links=[],
                        metadata=metadata
                    )

                    # Basic validation/cleanup
                    if prov.hierarchy_level is not None:
                        try:
                            prov.hierarchy_level = int(prov.hierarchy_level)
                        except (ValueError, TypeError):
                            print(f"Warning: Provision {prov.id} has non-integer hierarchy_level: {prov.hierarchy_level}. Setting to None.")
                            prov.hierarchy_level = None
                        
                    if prov.id and prov.regulation_id:
                        self.provisions[prov.id] = prov
                        if prov.regulation_id in self.regulations:
                            if not hasattr(self.regulations[prov.regulation_id], 'provisions') or self.regulations[prov.regulation_id].provisions is None:
                                self.regulations[prov.regulation_id].provisions = []
                            self.regulations[prov.regulation_id].provisions.append(prov.id)
                            
                        # --- Link Roles/Experts to this Provision --- 
                        # Find Role IDs corresponding to the names found in axis12
                        # This requires a lookup map (name -> ID) or filtering roles by name
                        # For now, this step is skipped - needs name-to-ID mapping logic
                        # role_ids_for_provision = self._map_role_names_to_ids(roles_responsible_names)
                        # for role_id in role_ids_for_provision:
                        #    if role_id in self.roles and prov.id not in self.roles[role_id].provisions:
                        #        self.roles[role_id].provisions.append(prov.id)
                        
                        # TODO: Add similar logic for linking Experts based on provision fields/axes if needed

        except FileNotFoundError:
            print(f"Warning: Provisions file (expecting nodes) not found at {file_path}")
        except Exception as e:
            print(f"Error loading provisions (from nodes) from {file_path}: {e}")

    # --- Linking Method (Called after all loading) ---
    def _link_entities(self):
        """Links related entities after initial loading. 
           - Maps role names in Provision.roles_responsible to Role IDs.
           - Populates Role.provisions list.
        """
        print("Starting entity linking...")
        # Create a map of role names to IDs for efficient lookup
        role_name_to_id = {role.name.lower(): role.id for role in self.roles.values() if role.name}
        if not role_name_to_id:
            print("Warning: No roles loaded or roles have no names. Cannot link provisions to roles.")
            # return # Optionally return if no roles to map

        provisions_linked_count = 0
        roles_updated_count = 0
        
        for provision in self.provisions.values():
            role_ids_for_provision = []
            # Ensure roles_responsible is a list and contains strings (names for now)
            if isinstance(provision.roles_responsible, list):
                original_role_names = list(provision.roles_responsible) # Keep original for iteration
                provision.roles_responsible = [] # Reset to store IDs
                
                for role_name in original_role_names:
                    if not isinstance(role_name, str):
                        print(f"Warning: Non-string role name found in provision {provision.id}: {role_name}. Skipping.")
                        continue
                        
                    role_id = role_name_to_id.get(role_name.lower()) # Case-insensitive lookup
                    if role_id:
                        role_ids_for_provision.append(role_id)
                        # Add provision ID to the Role object's list, avoiding duplicates
                        if role_id in self.roles:
                            if provision.id not in self.roles[role_id].provisions:
                                self.roles[role_id].provisions.append(provision.id)
                                roles_updated_count += 1 # Count role updates
                        else:
                             print(f"Warning: Role ID {role_id} found for name '{role_name}' but Role object not found.")
                    else:
                        print(f"Warning: Could not find Role ID for role name '{role_name}' in provision {provision.id}")
            
            # Update provision object to store Role IDs instead of names
            if role_ids_for_provision:
                 provision.roles_responsible = role_ids_for_provision
                 provisions_linked_count += 1
            # else: provision.roles_responsible remains an empty list if no mapping occurred
            
        print(f"Entity linking complete. Provisions updated with Role IDs: {provisions_linked_count}. Roles updated with Provision IDs: {roles_updated_count}.")
        
        # TODO: Add similar logic for Experts if they need linking based on provision data

    def load_mappings(self, file_path: str):
        # Load Spiderweb, Honeycomb, Octopus nodes - assuming keys in YAML
        try:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                for item in data.get('spiderwebs', []):
                    node = SpiderwebNode(**item)
                    self.spiderwebs[node.id] = node
                    # Optionally link back to provisions here if needed
                for item in data.get('honeycombs', []):
                    node = HoneycombNode(**item)
                    self.honeycombs[node.id] = node
                for item in data.get('octopuses', []):
                    node = OctopusNode(**item)
                    self.octopuses[node.id] = node
        except FileNotFoundError:
            print(f"Warning: Mappings file not found at {file_path}")
        except Exception as e:
            print(f"Error loading mappings from {file_path}: {e}")

    # --- Renamed/Refactored Access Methods ---

    def get_provision_by_id(self, provision_id: str) -> Optional[Provision]:
        return self.provisions.get(provision_id)

    def get_regulation_by_id(self, regulation_id: str) -> Optional[Regulation]:
        return self.regulations.get(regulation_id)
        
    def get_role_by_id(self, role_id: str) -> Optional[Role]:
        return self.roles.get(role_id)
        
    def get_expert_by_id(self, expert_id: str) -> Optional[Expert]:
        return self.experts.get(expert_id)

    def get_all_regulations(self) -> List[Regulation]:
        return list(self.regulations.values())
        
    def get_all_provisions(self) -> List[Provision]:
        return list(self.provisions.values())
        
    # --- Updated Query Method ---
        
    def query_provisions(self, 
                           regulation_id: Optional[str] = None,
                           jurisdiction: Optional[str] = None,
                           tag: Optional[str] = None,
                           role_id: Optional[str] = None,
                           min_confidence: Optional[float] = None,
                           compliance_tag: Optional[str] = None
                          ) -> List[Provision]:
        """Query provisions based on various criteria including confidence and compliance tags."""
        matches = list(self.provisions.values())
        if regulation_id:
            matches = [p for p in matches if p.regulation_id == regulation_id]
        if jurisdiction:
            matches = [p for p in matches if p.jurisdiction == jurisdiction]
        if tag:
            matches = [p for p in matches if p.tags and tag in p.tags]
        if role_id:
            matches = [p for p in matches if p.roles_responsible and role_id in p.roles_responsible]
        if min_confidence is not None:
            matches = [
                p for p in matches 
                if p.metadata and isinstance(p.metadata.get('confidence'), (int, float)) 
                and p.metadata['confidence'] >= min_confidence
            ]
        if compliance_tag:
            matches = [p for p in matches if p.crosswalks and compliance_tag in p.crosswalks]
            
        return matches

    # --- Kept old methods temporarily if needed, otherwise remove --- 
    def get_node_by_id(self, node_id: str) -> Optional[KnowledgeNode]:
        print("Warning: get_node_by_id is deprecated, use get_provision_by_id etc.")
        provision = self.get_provision_by_id(node_id)
        if provision:
            return KnowledgeNode(
                node_id=provision.id,
                pillar_id=provision.regulation_id,
                label=provision.title,
                description=provision.text,
                axes={
                    'axis3': provision.section, # Add reverse mapping for section
                    'axis4': provision.hierarchy_level,
                    'axis7': provision.octopus_refs,
                    'axis8': provision.crosswalks, 
                    'axis13': {'tags': provision.tags}, # Reconstruct axis13 structure
                }, 
                metadata=NodeMetadata(**provision.metadata) if provision.metadata else NodeMetadata(), # Map metadata back
            )
        return None

    def get_pillar_by_id(self, pillar_id: str) -> Optional[Pillar]:
        print("Warning: get_pillar_by_id is deprecated, use get_regulation_by_id etc.")
        regulation = self.get_regulation_by_id(pillar_id)
        if regulation:
             # Attempt a basic conversion back to Pillar
             return Pillar(
                 id=regulation.id,
                 name=regulation.title,
                 description=regulation.summary
             )
        return None
        
    def get_all_pillars(self) -> List[Pillar]:
        print("Warning: get_all_pillars is deprecated, use get_all_regulations.")
        return []

    def query_nodes(self, **axis_filters) -> List[KnowledgeNode]:
        print("Warning: query_nodes is deprecated, use query_provisions.")
        # This would need significant refactoring to map axis_filters to Provision fields
        return []

    def query_confidence(self, min_confidence: float) -> List[KnowledgeNode]:
        print("Warning: query_confidence is deprecated.")
        # Confidence might be on metadata or specific axes now
        return []
