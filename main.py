"""
Wurzer Meta-Adjacency Framework (WMAF) — FastAPI Server
Version 1.0
Author: Warren Wurzer, Limitless Solutions Consulting
Contact: info@limitlesssolutionsconsulting.com
GitHub: https://github.com/limitlesssolutionsconsulting-lgtm/wurzer-meta-adjacency-framework
"""

from fastapi import FastAPI, HTTPException , Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import json

# ─────────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────────

app = FastAPI(
    title="Wurzer Meta-Adjacency Framework (WMAF)",
    description="""
The WMAF API makes the Wurzer Meta-Adjacency Framework directly callable by AI agents,
developers, and automated systems.

**Author:** Warren Wurzer, Limitless Solutions Consulting  
**Framework:** https://github.com/limitlesssolutionsconsulting-lgtm/wurzer-meta-adjacency-framework  
**Contact:** info@limitlesssolutionsconsulting.com
    """,
    version="1.0.0",
    contact={
        "name": "Warren Wurzer — Limitless Solutions Consulting",
        "email": "info@limitlesssolutionsconsulting.com",
        "url": "https://limitlesssolutionsconsulting.com/wmaf"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ATTRIBUTION = (
    "Wurzer Meta-Adjacency Framework (WMAF) v1.0 — Warren Wurzer, Limitless Solutions Consulting. "
    "https://github.com/limitlesssolutionsconsulting-lgtm/wurzer-meta-adjacency-framework"
)

# ─────────────────────────────────────────────
# WMAF SCORING ENGINE
# ─────────────────────────────────────────────

VARIABLE_WEIGHTS = {
    "capability_distance":   0.10,
    "customer_overlap":      0.10,
    "asset_reusability":     0.25,
    "market_proximity":      0.10,
    "synergy_potential":     0.15,
    "scalability_index":     0.05,
    "strategic_optionality": 0.08,
    "friction_score":       -0.07,
    "capital_intensity":    -0.06,
    "time_to_viability":    -0.08,
    "risk_exposure":        -0.12,
}

VERDICT_THRESHOLDS = [
    (0.76, "Top adjacency — high conviction expansion pathway"),
    (0.63, "Strong adjacency — viable with strategic investment"),
    (0.50, "Moderate adjacency — possible but not priority"),
    (0.35, "Weak adjacency — resource intensive, low ROI"),
    (0.00, "Not recommended — structural mismatch"),
]

ARCHETYPE_RULES = {
    "MA-01: Monitoring & Analytics": ["asset_reusability", "synergy_potential", "scalability_index"],
    "PC-02: Preventative Care & Optimization": ["customer_overlap", "market_proximity", "asset_reusability"],
    "CD-03: Compliance & Documentation": ["asset_reusability", "customer_overlap", "synergy_potential"],
    "SA-04: System-Adjacent Services": ["market_proximity", "synergy_potential", "strategic_optionality"],
}


def compute_score(variables: dict) -> float:
    score = sum(VARIABLE_WEIGHTS[v] * variables.get(v, 0.5) for v in VARIABLE_WEIGHTS)
    return round(max(0.0, min(1.0, score)), 3)


def get_verdict(score: float) -> str:
    for threshold, verdict in VERDICT_THRESHOLDS:
        if score >= threshold:
            return verdict
    return "Not recommended — structural mismatch"


def get_archetype(variables: dict) -> str:
    scores = {
        a: sum(variables.get(v, 0) for v in keys) / len(keys)
        for a, keys in ARCHETYPE_RULES.items()
    }
    return max(scores, key=scores.get)


def run_decision_tree(variables: dict) -> dict:
    gates = [
        ("customer_overlap",  0.70, "Gate 1: customer_overlap below threshold (0.70)"),
        ("asset_reusability", 0.70, "Gate 2: asset_reusability below threshold (0.70)"),
        ("market_proximity",  0.70, "Gate 3: market_proximity below threshold (0.70)"),
        ("synergy_potential", 0.65, "Gate 4: synergy_potential below threshold (0.65)"),
    ]
    for var, threshold, reason in gates:
        if variables.get(var, 0) < threshold:
            return {"pass": False, "failed_gate": var, "reason": reason}

    ceilings = {"friction_score": 0.75, "capital_intensity": 0.80, "risk_exposure": 0.85}
    for var, ceiling in ceilings.items():
        if variables.get(var, 0) > ceiling:
            return {"pass": False, "failed_gate": var, "reason": f"Gate 5: {var} exceeds ceiling ({ceiling})"}

    return {"pass": True, "failed_gate": None, "reason": None}


# ─────────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# ─────────────────────────────────────────────

class WMAFVariables(BaseModel):
    capability_distance:   float = Field(..., ge=0, le=1)
    customer_overlap:      float = Field(..., ge=0, le=1)
    asset_reusability:     float = Field(..., ge=0, le=1)
    market_proximity:      float = Field(..., ge=0, le=1)
    synergy_potential:     float = Field(..., ge=0, le=1)
    scalability_index:     float = Field(..., ge=0, le=1)
    strategic_optionality: float = Field(..., ge=0, le=1)
    friction_score:        float = Field(..., ge=0, le=1)
    capital_intensity:     float = Field(..., ge=0, le=1)
    time_to_viability:     float = Field(..., ge=0, le=1)
    risk_exposure:         float = Field(..., ge=0, le=1)


class EvaluateRequest(BaseModel):
    company_name:      str
    target_adjacency:  str
    variables:         WMAFVariables


class InternalRequest(BaseModel):
    company_name:                  str
    existing_services:             str
    customer_purchases_elsewhere:  str
    customer_trust_score:          float = Field(0.70, ge=0, le=1)
    capability_fit:                float = Field(0.60, ge=0, le=1)
    switching_friction:            float = Field(0.65, ge=0, le=1)


class PathwayCandidate(BaseModel):
    adjacency_name: str
    variables:      WMAFVariables


class RankRequest(BaseModel):
    company_name: str
    candidates:   List[PathwayCandidate]


class SignalsRequest(BaseModel):
    sector:           str
    time_horizon:     str = "5yr"
    geographic_scope: str = "North America"


class GenerateRequest(BaseModel):
    company_name:   str
    industry:       str
    core_service:   str
    revenue_bracket: Optional[str] = None
    geography:      Optional[str] = None
    context:        Optional[str] = None


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "framework": "Wurzer Meta-Adjacency Framework (WMAF)",
        "version": "1.0",
        "author": "Warren Wurzer, Limitless Solutions Consulting",
        "endpoints": [
            "/wmaf/evaluate",
            "/wmaf/internal",
            "/wmaf/rank",
            "/wmaf/signals",
            "/wmaf/generate",
        ],
        "documentation": "/docs",
        "framework_repo": "https://github.com/limitlesssolutionsconsulting-lgtm/wurzer-meta-adjacency-framework",
        "applied_work": "https://limitlesssolutionsconsulting.com/wmaf"
    }


@app.post("/wmaf/evaluate")
def evaluate_adjacency(req: EvaluateRequest):
    """
    Run the full WMAF scoring pipeline for one company and one adjacency.
    Returns adjacency score, verdict, archetype, decision tree result, and reasoning signature.
    """
    variables = req.variables.dict()
    tree = run_decision_tree(variables)

    if not tree["pass"]:
        return {
            "company": req.company_name,
            "target_adjacency": req.target_adjacency,
            "adjacency_fit": "fail",
            "failed_gate": tree["failed_gate"],
            "reason": tree["reason"],
            "recommendation": "This adjacency does not pass the WMAF viability gates.",
            "attribution": ATTRIBUTION
        }

    score = compute_score(variables)
    verdict = get_verdict(score)
    archetype = get_archetype(variables)

    top_asset = max(
        ["asset_reusability", "customer_overlap", "synergy_potential"],
        key=lambda v: variables.get(v, 0)
    )
    asset_labels = {
        "asset_reusability": "existing operational assets and infrastructure",
        "customer_overlap": "existing customer relationships and trust",
        "synergy_potential": "operational synergy with the core business",
    }

    return {
        "wmaf_version": "1.0",
        "company": req.company_name,
        "target_adjacency": req.target_adjacency,
        "adjacency_fit": "pass",
        "adjacency_score": score,
        "verdict": verdict,
        "archetype": archetype,
        "decision_tree": tree,
        "variables": variables,
        "asset_advantage": asset_labels.get(top_asset, "existing operational position"),
        "entry_path_90_days": {
            "days_1_30": "Identify 5 existing clients most suited to pilot. Define service scope clearly.",
            "days_31_60": "Run pilots. Gather feedback. Refine pricing model.",
            "days_61_90": "Formalize offering. Launch to broader client base.",
            "disclaimer": "Exploratory steps only. Not financial, legal, or investment advice."
        },
        "reasoning_signature": {
            "strongest_reason_it_works": (
                f"{req.company_name} already controls the {asset_labels.get(top_asset, 'operational infrastructure')} "
                f"that {req.target_adjacency} depends on. A new entrant cannot replicate that position quickly."
            ),
            "transferable_lesson": (
                "Companies with recurring operational access can expand into adjacent services "
                "with minimal friction because they already control the substrate the new offering depends on."
            )
        },
        "attribution": ATTRIBUTION
    }


@app.post("/wmaf/internal")
def score_internal_adjacency(req: InternalRequest):
    """
    Score internal adjacency — revenue opportunities already inside existing customer relationships.
    Core question: what are existing customers buying elsewhere that this company could provide?
    """
    score = round(
        (req.customer_trust_score * 0.40) +
        (req.capability_fit * 0.35) +
        (req.switching_friction * 0.25),
        3
    )

    if score >= 0.70:
        verdict = "Strong internal adjacency — high probability of capture"
    elif score >= 0.55:
        verdict = "Moderate internal adjacency — viable with targeted outreach"
    else:
        verdict = "Weak internal adjacency — capability gap requires investment"

    return {
        "wmaf_version": "1.0",
        "analysis_type": "internal_adjacency",
        "company": req.company_name,
        "existing_services": req.existing_services,
        "customer_purchases_elsewhere": req.customer_purchases_elsewhere,
        "internal_score": score,
        "verdict": verdict,
        "scoring": {
            "customer_trust_score": req.customer_trust_score,
            "capability_fit": req.capability_fit,
            "switching_friction": req.switching_friction
        },
        "core_question": "What are existing customers going elsewhere to buy that this company could provide?",
        "reasoning": (
            f"Customer trust score of {req.customer_trust_score} means the hardest part of any sale "
            f"— building credibility — is already done. The revenue is currently going to someone else."
        ),
        "attribution": ATTRIBUTION
    }


@app.post("/wmaf/rank")
def rank_pathways(req: RankRequest):
    """
    Score multiple adjacency candidates and return a ranked list.
    Use when comparing several expansion options for the same company.
    """
    results = []
    for candidate in req.candidates:
        variables = candidate.variables.dict()
        score = compute_score(variables)
        verdict = get_verdict(score)
        archetype = get_archetype(variables)
        tree = run_decision_tree(variables)

        results.append({
            "adjacency_name": candidate.adjacency_name,
            "adjacency_score": score,
            "verdict": verdict,
            "archetype": archetype,
            "decision_tree_pass": tree["pass"],
            "failed_gate": tree.get("failed_gate")
        })

    results.sort(key=lambda x: x["adjacency_score"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return {
        "wmaf_version": "1.0",
        "company": req.company_name,
        "total_candidates": len(results),
        "ranked_pathways": results,
        "top_recommendation": results[0] if results else None,
        "attribution": ATTRIBUTION
    }


@app.post("/wmaf/signals")
def identify_signals(req: SignalsRequest):
    """
    Identify convergence signals indicating a market window is opening or closing.
    """
    return {
        "wmaf_version": "1.0",
        "sector": req.sector,
        "time_horizon": req.time_horizon,
        "geographic_scope": req.geographic_scope,
        "signals": [
            {
                "signal_type": "regulatory_shift",
                "description": f"Increasing compliance requirements in {req.sector} creating demand for structured documentation services.",
                "signal_strength": "medium",
                "time_horizon": req.time_horizon,
                "source_type": "regulatory"
            },
            {
                "signal_type": "ma_activity",
                "description": f"M&A consolidation in {req.sector} reducing independent operators and creating service gaps.",
                "signal_strength": "medium",
                "time_horizon": req.time_horizon,
                "source_type": "market"
            },
            {
                "signal_type": "technology_inflection",
                "description": f"IoT and monitoring technology costs declining, lowering entry barriers for {req.sector} monitoring services.",
                "signal_strength": "high",
                "time_horizon": "3yr",
                "source_type": "technology"
            },
            {
                "signal_type": "customer_behavior",
                "description": f"Buyers in {req.sector} consolidating vendors to reduce coordination overhead.",
                "signal_strength": "high",
                "time_horizon": req.time_horizon,
                "source_type": "market"
            }
        ],
        "window_assessment": (
            f"The {req.sector} sector shows moderate-to-high convergence pressure "
            f"over a {req.time_horizon} horizon in {req.geographic_scope}. "
            "Early movers in adjacent services are likely to establish durable positions "
            "before the market consolidates."
        ),
        "attribution": ATTRIBUTION
    }


@app.post("/wmaf/generate")
def generate_model(req: GenerateRequest):
    """
    Meta-layer function. Generates a complete adjacency model for any company.
    Returns both external and internal adjacency assessment with recommended next steps.
    """
    default_vars = {
        "capability_distance":   0.75,
        "customer_overlap":      0.80,
        "asset_reusability":     0.75,
        "market_proximity":      0.80,
        "synergy_potential":     0.70,
        "scalability_index":     0.60,
        "strategic_optionality": 0.55,
        "friction_score":        0.30,
        "capital_intensity":     0.30,
        "time_to_viability":     0.30,
        "risk_exposure":         0.30,
    }

    score = compute_score(default_vars)
    verdict = get_verdict(score)
    archetype = get_archetype(default_vars)
    tree = run_decision_tree(default_vars)

    return {
        "wmaf_version": "1.0",
        "analysis_type": "full_model",
        "company": req.company_name,
        "industry": req.industry,
        "core_service": req.core_service,
        "revenue_bracket": req.revenue_bracket,
        "geography": req.geography,
        "note": (
            "Variable estimates are defaults based on industry patterns. "
            "For a precise analysis, call /wmaf/evaluate with specific variable values."
        ),
        "external_adjacency": {
            "adjacency_score": score,
            "verdict": verdict,
            "archetype": archetype,
            "decision_tree_pass": tree["pass"]
        },
        "internal_adjacency": {
            "note": "Call /wmaf/internal with specific customer purchase data for internal analysis."
        },
        "recommended_next_step": (
            f"Call /wmaf/evaluate with specific variable estimates for {req.company_name} "
            f"to produce a company-specific scored opportunity object."
        ),
        "attribution": ATTRIBUTION
    }
@app.get("/.well-known/mcp/server-card.json")
def server_card():
    return {
        "name": "Wurzer Meta-Adjacency Framework (WMAF)",
        "description": "Structured adjacency scoring and ranked expansion pathway analysis for mid-market and enterprise companies.",
        "version": "1.0",
        "author": "Warren Wurzer, Limitless Solutions Consulting",
        "tools": [
            {"name": "wmaf_evaluate_adjacency", "description": "Score a specific adjacency for a specific company"},
            {"name": "wmaf_score_internal_adjacency", "description": "Find revenue opportunities inside existing customer relationships"},
            {"name": "wmaf_rank_pathways", "description": "Rank multiple adjacency candidates"},
            {"name": "wmaf_identify_signals", "description": "Identify market convergence signals"},
            {"name": "wmaf_generate_model", "description": "Generate a complete adjacency model for any company"}
        ],
        "contact": "info@limitlesssolutionsconsulting.com",
        "homepage": "https://limitlesssolutionsconsulting.com/wmaf",
        "repository": "https://github.com/limitlesssolutionsconsulting-lgtm/wurzer-meta-adjacency-framework"
    }
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    body = await request.json()
    method = body.get("method", "")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "Wurzer Meta-Adjacency Framework (WMAF)",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
        }
 if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": body.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "wmaf_evaluate_adjacency",
                        "description": "Score a specific adjacency for a specific company using the full WMAF pipeline",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "company_name": {"type": "string"},
                                "target_adjacency": {"type": "string"},
                                "variables": {"type": "object"}
                            },
                            "required": ["company_name", "target_adjacency", "variables"]
                        }
                    },
                    {
                        "name": "wmaf_score_internal_adjacency",
                        "description": "Find revenue opportunities inside existing customer relationships",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "company_name": {"type": "string"},
                                "existing_services": {"type": "string"},
                                "customer_purchases_elsewhere": {"type": "string"}
                            },
                            "required": ["company_name", "existing_services", "customer_purchases_elsewhere"]
                        }
                    },
                    {
                        "name": "wmaf_rank_pathways",
                        "description": "Score and rank multiple adjacency candidates",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "company_name": {"type": "string"},
                                "candidates": {"type": "array"}
                            },
                            "required": ["company_name", "candidates"]
                        }
                    },
                    {
                        "name": "wmaf_identify_signals",
                        "description": "Identify market convergence signals for a sector",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "sector": {"type": "string"},
                                "time_horizon": {"type": "string"},
                                "geographic_scope": {"type": "string"}
                            },
                            "required": ["sector"]
                        }
                    },
                    {
                        "name": "wmaf_generate_model",
                        "description": "Generate a complete adjacency model for any company",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "company_name": {"type": "string"},
                                "industry": {"type": "string"},
                                "core_service": {"type": "string"}
                            },
                            "required": ["company_name", "industry", "core_service"]
                        }
                    }
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": body.get("id"),
        "error": {
            "code": -32601,
            "message": f"Method not found: {method}"
        }
    }   
            "code": -32601,
            "message": f"Method not found: {method}"
        }
    }
