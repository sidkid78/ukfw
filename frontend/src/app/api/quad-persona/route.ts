import { NextRequest, NextResponse } from "next/server";
export async function POST(req: NextRequest) {
    const body = await req.json();
    const resp = await fetch("http://localhost:8000/quad-persona", {
        method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)
    });
    return NextResponse.json(await resp.json());
}
