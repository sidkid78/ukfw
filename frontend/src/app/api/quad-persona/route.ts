import { NextRequest, NextResponse } from "next/server";
export async function POST(req: NextRequest) {
    const body = await req.json();
    const backendUrl = process.env.BACKEND_API_URL || "http://localhost:8000/reason/quad"; 
    const resp = await fetch(backendUrl, { 
        method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)
    });
    if (!resp.ok) {
        const errorText = await resp.text().catch(() => `Backend responded with status ${resp.status}`);
        console.error(`Backend API error (${resp.status}): ${errorText}`);
        return NextResponse.json({ error: `Failed to reach backend: ${errorText}` }, { status: resp.status });
    }
    return NextResponse.json(await resp.json());
}
