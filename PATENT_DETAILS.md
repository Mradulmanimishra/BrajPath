# PATENT APPLICATION DETAILS
## BrajPath: Multilingual AI-Powered Pilgrimage Guidance System via Conversational Messaging Interface

---

## SECTION 1: TITLE OF INVENTION

**"System and Method for Providing Real-Time, Multilingual, Context-Aware Pilgrimage Guidance Through a Conversational Messaging Interface Using a Registry-Based Finite State Machine and Persistent Session Context Engine"**

---

## SECTION 2: APPLICANT DETAILS

| Field | Details |
|-------|---------|
| Inventor Name | Mradul Mani Mishra |
| Project Name | BrajPath (also referred to as "Braj Sahayak") |
| Repository | https://github.com/Mradulmanimishra/BrajPath |
| Application Type | Software / Computer-Implemented Invention |
| Field | Artificial Intelligence, Conversational Systems, Religious Tourism Technology |
| Country | India |
| Filing Authority | Indian Patent Office (IPO) under The Patents Act, 1970 |

---

## SECTION 3: FIELD OF THE INVENTION

This invention relates to a **computer-implemented conversational guidance system** specifically designed for religious pilgrimage tourism. More particularly, it relates to a **WhatsApp-based multilingual chatbot** that uses a **Registry-Based Finite State Machine (FSM)** and a **Persistent Session Context Engine** to deliver real-time, personalized temple guidance to pilgrims visiting the Mathura-Vrindavan (Braj) region of India.

---

## SECTION 4: BACKGROUND OF THE INVENTION

### 4.1 Problem Statement

The Mathura-Vrindavan region of Uttar Pradesh, India, receives over **50 million pilgrims annually**, making it one of the most visited religious destinations in the world. Despite this scale, pilgrims face severe **information asymmetry**:

1. **Dynamic Temple Timings** — Temple opening hours change seasonally (summer/winter/monsoon) and during festivals. No centralized, verified, real-time source exists.

2. **Language Barriers** — Pilgrims arrive from across India speaking Hindi, Bengali, Tamil, English, and other languages. Local information is predominantly in Hindi only.

3. **Transport Exploitation** — Pilgrims unfamiliar with local transport are routinely overcharged by auto-rickshaw and e-rickshaw operators. No standardized fare guide exists.

4. **Navigation Complexity** — The narrow lanes of Vrindavan and Mathura are difficult to navigate. Pilgrims lack reliable last-mile routing information.

5. **Digital Divide** — A large proportion of pilgrims are elderly or semi-literate and cannot use complex smartphone apps. However, **WhatsApp penetration in India exceeds 500 million users**, making it the most accessible digital interface.

### 4.2 Limitations of Prior Art

- **Generic chatbots** (e.g., Dialogflow, Rasa) are not domain-specific and require NLP training data not available for this niche.
- **Temple websites** are static, not conversational, and rarely mobile-optimized.
- **Google Maps** provides routing but not temple-specific timing, advisory, or fare information.
- **Existing WhatsApp bots** for tourism are either English-only or lack persistent session memory.
- **No prior system** combines multilingual support, seasonal timing logic, community fare guides, and persistent user context in a single WhatsApp interface for religious tourism.

---

## SECTION 5: SUMMARY OF THE INVENTION

BrajPath is a **novel computer-implemented system** comprising:

1. A **Registry-Based Finite State Machine (FSM)** for managing multi-turn conversational flows over WhatsApp.
2. A **Persistent Session Context Engine** that stores and retrieves user preferences, interaction history, and geospatial memory across sessions.
3. A **Multilingual Translation Layer** supporting English, Hindi, Bengali, and Tamil.
4. A **Seasonal Temple Timing Engine** that dynamically selects the correct schedule based on current date, season, and festival overrides.
5. A **Community Fare Intelligence Module** providing verified transport pricing.
6. A **Secure Webhook Gateway** with cryptographic request validation via HMAC-SHA1 (Twilio Signature Validation).
7. A **Structured Relational Data Model** with 12 normalized database tables for temples, schedules, routes, advisories, partners, and analytics.

---

## SECTION 6: DETAILED DESCRIPTION OF THE INVENTION

### 6.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        PILGRIM (User)                           │
│                    WhatsApp Mobile App                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ WhatsApp Message
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   TWILIO API GATEWAY                            │
│         (HMAC-SHA1 Signature Validation Layer)                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP POST Webhook
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              FASTAPI ASYNC WEBHOOK LAYER                        │
│   • Phone number validation (E.164 format)                      │
│   • Request authentication                                      │
│   • Response time telemetry                                     │
│   • TwiML response formatting                                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│           REGISTRY-BASED STATE MACHINE ENGINE                   │
│                                                                 │
│  ┌─────────────────┐    ┌──────────────────────────────────┐   │
│  │  HANDLER        │    │  REGISTERED STATE HANDLERS       │   │
│  │  REGISTRY       │───▶│  • language_select               │   │
│  │  (dict-based    │    │  • main_menu                     │   │
│  │   dispatch)     │    │  • temple_area_select            │   │
│  └─────────────────┘    │  • area_temple_select            │   │
│                         │  • route_from_select             │   │
│  ┌─────────────────┐    │  • partner_category_select       │   │
│  │  CONTEXT        │    │  • partner_list                  │   │
│  │  MANAGER        │    └──────────────────────────────────┘   │
│  │  (Session JSON) │                                           │
│  └─────────────────┘                                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              TEMPLE SERVICE LAYER                               │
│   • Seasonal timing engine                                      │
│   • Festival override resolver                                  │
│   • Route & fare calculator                                     │
│   • Advisory formatter                                          │
│   • Partner directory                                           │
│   • Multilingual translation loader                             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              PERSISTENCE LAYER (SQLAlchemy ORM)                 │
│                                                                 │
│  temples │ schedules │ festival_overrides │ temple_advisories   │
│  route_points │ routes │ fare_guides                            │
│  partner_categories │ partners                                  │
│  user_sessions │ support_requests │ query_logs                  │
└─────────────────────────────────────────────────────────────────┘
```

---

### 6.2 Novel Component 1: Registry-Based Finite State Machine

**Technical Description:**

The core innovation is a **decorator-based handler registry** that maps conversation states to handler functions at module load time, enabling O(1) dispatch without nested if-else chains.

**Implementation:**

```python
# Handler type definition
HandlerType = Callable[[str, UserSession, ContextManager, str, str, Session], str]
HANDLER_REGISTRY: dict[str, HandlerType] = {}

# Registration decorator
def register_handler(state: str) -> Callable[[HandlerType], HandlerType]:
    def decorator(handler: HandlerType) -> HandlerType:
        HANDLER_REGISTRY[state] = handler
        return handler
    return decorator

# Usage
@register_handler("temple_area_select")
def _handle_temple_area_select(...) -> str:
    ...

# Dispatch (O(1) lookup)
handler = HANDLER_REGISTRY.get(session.current_state)
if handler:
    return handler(text, session, ctx, wa_number, incoming, db)
```

**State Transition Graph:**

```
[ANY MESSAGE] ──(entry trigger)──▶ main_menu
                                       │
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
              ▼                        ▼                        ▼
    temple_area_select          partner_category_select   language_select
              │                        │
              ▼                        ▼
    area_temple_select           partner_list
              │
    ┌─────────┴──────────┐
    │                    │
    ▼                    ▼
 main_menu        route_from_select
(timing/advisory)        │
                         ▼
                      main_menu
                     (route shown)
```

**Novelty:** Unlike traditional chatbot frameworks that use linear decision trees or NLP intent classifiers, this system uses a **compile-time registered dispatch table** that is:
- Extensible without modifying core dispatch logic
- Testable in isolation per state
- O(1) lookup regardless of number of states

---

### 6.3 Novel Component 2: Persistent Session Context Engine

**Technical Description:**

A **dual-layer persistence model** combining:
1. **Relational state** (SQL columns) for structured session data
2. **JSON context blob** for unstructured behavioral history

**SessionContext Pydantic Model:**
```python
class SessionContext(BaseModel):
    last_visited_area: Optional[str] = None
    last_visited_temple: Optional[str] = None
    preferred_city: Optional[str] = None
    interaction_history: list[str]   # Last 10 intents (sliding window)
    metadata: dict[str, Any]
```

**UserSession Database Schema:**
```
user_sessions table:
  wa_number          VARCHAR(30)  UNIQUE  -- WhatsApp identifier
  language_code      VARCHAR(10)          -- User's preferred language
  current_state      VARCHAR(60)          -- FSM current state
  prev_state         VARCHAR(60)          -- Previous state (for back navigation)
  selected_temple    VARCHAR(60)          -- Active temple context
  selected_area      VARCHAR(50)          -- Active area context
  selected_route_from VARCHAR(60)         -- Route origin context
  pending_action     VARCHAR(20)          -- Cross-state action context
  context_data       TEXT                 -- JSON blob (SessionContext)
  message_count      INTEGER              -- Engagement metric
  last_seen_at       DATETIME             -- Activity timestamp
```

**Context-Aware Suggestion Algorithm:**
```python
def get_suggested_area(self) -> Optional[str]:
    # Returns last visited area OR preferred city
    # Used to provide personalized navigation hints
    return self.context.last_visited_area or self.context.preferred_city
```

**Novelty:** The system maintains a **sliding window of the last 10 user intents** serialized as JSON within a relational database, enabling behavioral pattern analysis without a separate NoSQL store. The `pending_action` field enables **cross-state intent propagation** — a user's choice (e.g., "get route") is preserved across multiple navigation steps.

---

### 6.4 Novel Component 3: Seasonal Temple Timing Engine

**Technical Description:**

Temple timings in India vary by season and festival. The system implements a **three-tier schedule resolution algorithm**:

```
Priority 1: Festival Override (date-range based)
    ↓ (if no active festival)
Priority 2: Seasonal Schedule (summer/winter/monsoon)
    ↓ (if no seasonal schedule)
Priority 3: General Schedule (year-round fallback)
```

**Season Detection Logic:**
```python
def _current_season(now_ist: datetime) -> str:
    m = now_ist.month
    if m in (11, 12, 1, 2):  return "winter"
    if m in (7, 8, 9, 10):   return "monsoon"
    return "summer"           # March–June
```

**Open/Closed Real-Time Logic:**
```python
def _is_open(schedule, now_ist: datetime) -> bool:
    t = now_ist.time()
    morning_open = schedule.open_morning <= t <= schedule.close_morning
    evening_open = schedule.open_evening <= t <= schedule.close_evening
    bhog_closed  = schedule.bhog_start <= t <= schedule.bhog_end  # Midday closure
    return (morning_open or evening_open) and not bhog_closed
```

**Novelty:** The **Bhog period** (midday ritual closure unique to Vaishnava temples) is modeled as a first-class entity in the schedule, not a simple time gap. Festival overrides take precedence over seasonal schedules, enabling accurate real-time status during major Hindu festivals (Janmashtami, Holi, Radhashtami, etc.).

---

### 6.5 Novel Component 4: Multilingual Translation Architecture

**Technical Description:**

A **lazy-loaded, JSON-based translation system** supporting 4 languages with graceful English fallback:

```python
def tr(key: str, lang: str) -> str:
    data = _load_translations()  # Cached after first load
    return (
        data.get(key, {}).get(lang)      # Try requested language
        or data.get(key, {}).get("en")   # Fallback to English
        or f"[{key}]"                    # Debug fallback
    )
```

**Supported Languages:**
| Code | Language | Script |
|------|----------|--------|
| en | English | Latin |
| hi | Hindi | Devanagari |
| bn | Bengali | Bengali |
| ta | Tamil | Tamil |

**Database-Level Multilingual Fields:**
Every content entity (Temple, Route, RoutePoint, TempleAdvisory) stores translations as parallel columns:
```
name_en, name_hi, name_bn, name_ta
message_en, message_hi, message_bn, message_ta
route_text_en, route_text_hi, route_text_bn, route_text_ta
```

**Novelty:** The system uses **column-per-language** storage (not a separate translations table) for O(1) retrieval without JOIN operations, optimized for the read-heavy, low-latency requirements of a real-time messaging system.

---

### 6.6 Novel Component 5: Secure Webhook Gateway

**Technical Description:**

The system implements **HMAC-SHA1 cryptographic request validation** to prevent spoofing attacks:

```python
async def validate_twilio_request(request: Request) -> None:
    form = await request.form()
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    signature = request.headers.get("X-Twilio-Signature", "")
    request_url = _request_url_for_validation(request)
    if not validator.validate(request_url, dict(form), signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")
```

**URL Normalization for Reverse Proxy Environments:**
```python
def _request_url_for_validation(request: Request) -> str:
    # Reconstructs the public URL when behind a reverse proxy/CDN
    incoming = urlsplit(str(request.url))
    public_base = urlsplit(settings.PUBLIC_WEBHOOK_BASE_URL.rstrip("/"))
    return urlunsplit((public_base.scheme, public_base.netloc,
                       incoming.path, incoming.query, ""))
```

**Phone Number Validation (E.164):**
```python
def _validate_phone_number(wa_number: str) -> bool:
    cleaned = wa_number.replace("-", "").replace(" ", "")
    pattern = r"^\+?[0-9]{1,15}$"
    return bool(re.match(pattern, cleaned))
```

---

### 6.7 Novel Component 6: Analytics & Business Intelligence Layer

**Technical Description:**

Every user interaction is logged to a structured `query_logs` table:

```
query_logs table:
  wa_number        -- Anonymized user identifier
  language_code    -- Language used
  incoming_text    -- Raw user input
  detected_state   -- FSM state at time of query
  detected_intent  -- Classified user intent
  detected_entity  -- Extracted entity (temple, area, etc.)
  response_status  -- ok / error
  processing_ms    -- Response latency
  created_at       -- UTC timestamp
```

This enables:
- **Heatmap analysis** of most-queried temples
- **Language distribution** analytics
- **Peak usage time** identification
- **Error rate monitoring** per state
- **Conversion funnel** analysis (language select → temple query)

---

### 6.8 Database Schema (Complete)

**12 Normalized Tables:**

```
1. temples              — Temple master data with GPS coordinates
2. schedules            — Seasonal opening hours (summer/winter/monsoon/general)
3. festival_overrides   — Date-range based special timing overrides
4. temple_advisories    — Crowd, dress code, mobile, footwear advisories
5. route_points         — Transit hubs (railway stations, bus stands, ghats)
6. routes               — Transport options with fare ranges and directions
7. fare_guides          — Community-verified transport pricing
8. partner_categories   — Service categories (hotels, guides, transport)
9. partners             — Verified local service providers
10. user_sessions       — Persistent conversation state + context JSON
11. support_requests    — Human escalation tickets
12. query_logs          — Full interaction analytics log
```

---

### 6.9 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Web Framework | FastAPI | 0.115.0 | Async HTTP server |
| ASGI Server | Uvicorn | 0.30.6 | Production server |
| ORM | SQLAlchemy | 2.0.36 | Database abstraction |
| Database (Dev) | SQLite | Built-in | Local development |
| Database (Prod) | PostgreSQL + pg8000 | 1.31.2 | Production persistence |
| Messaging API | Twilio | 9.3.2 | WhatsApp integration |
| Data Validation | Pydantic | 2.x | Settings + context models |
| Timezone | pytz | 2024.2 | IST/UTC conversion |
| Language | Python | 3.11+ | Core runtime |
| Testing | pytest | 8.3.5 | Test suite (26 tests) |
| Linting | ruff | 0.6.9 | Code quality |

---

## SECTION 7: CLAIMS

### Independent Claims

**Claim 1:**
A computer-implemented system for providing multilingual pilgrimage guidance through a conversational messaging interface, comprising:
- a webhook gateway configured to receive and cryptographically validate incoming messages from a messaging platform;
- a registry-based finite state machine comprising a handler registry mapping conversation state identifiers to handler functions, wherein dispatch is performed in O(1) time;
- a persistent session context engine storing per-user conversation state, language preference, geospatial history, and a sliding-window interaction history in a relational database;
- a seasonal temple timing engine configured to resolve active schedules through a three-tier priority system comprising festival overrides, seasonal schedules, and general schedules;
- a multilingual translation layer supporting at least four languages with graceful fallback to a default language.

**Claim 2:**
The system of Claim 1, wherein the registry-based finite state machine uses Python decorator syntax to register handler functions at module load time, enabling extensibility without modification of core dispatch logic.

**Claim 3:**
The system of Claim 1, wherein the persistent session context engine stores unstructured behavioral data as a JSON blob within a relational database column, enabling behavioral pattern analysis without a separate document store.

**Claim 4:**
The system of Claim 1, wherein the seasonal temple timing engine models a midday ritual closure period (Bhog) as a first-class schedule entity distinct from morning and evening sessions.

**Claim 5:**
The system of Claim 1, wherein the multilingual translation layer uses column-per-language storage in relational database tables, enabling O(1) language-specific retrieval without JOIN operations.

### Dependent Claims

**Claim 6:**
The system of Claim 1, further comprising a community fare intelligence module storing verified transport pricing ranges for routes between transit hubs and religious sites.

**Claim 7:**
The system of Claim 1, further comprising an analytics layer that logs every user interaction with detected state, intent, entity, and response latency for business intelligence purposes.

**Claim 8:**
The system of Claim 1, wherein the webhook gateway implements URL normalization to reconstruct public-facing URLs when deployed behind a reverse proxy or content delivery network.

**Claim 9:**
The system of Claim 1, wherein the session context engine maintains a cross-state `pending_action` field enabling intent propagation across multiple conversation turns.

**Claim 10:**
A method for providing real-time temple guidance through a WhatsApp messaging interface, comprising:
- receiving a message via a cryptographically validated webhook;
- retrieving or creating a persistent user session from a relational database;
- dispatching the message to a registered state handler based on the current conversation state;
- resolving the active temple schedule through festival override, seasonal, and general schedule tiers;
- returning a multilingual formatted response within the character limits of the messaging platform.

---

## SECTION 8: ABSTRACT

BrajPath is a computer-implemented system and method for delivering real-time, multilingual, context-aware pilgrimage guidance to devotees visiting the Mathura-Vrindavan region of India through the WhatsApp messaging platform. The system employs a novel **Registry-Based Finite State Machine** using decorator-based handler registration for O(1) conversational state dispatch, a **Persistent Session Context Engine** combining relational state storage with JSON behavioral history, and a **three-tier Seasonal Temple Timing Engine** that resolves active schedules through festival overrides, seasonal schedules, and general fallbacks. The system supports four languages (English, Hindi, Bengali, Tamil) using a column-per-language relational storage model for low-latency retrieval. A secure HMAC-SHA1 webhook gateway prevents message spoofing. The system further comprises community-verified transport fare guides, temple advisories, partner service directories, and a full interaction analytics layer. The invention addresses the information asymmetry faced by over 50 million annual pilgrims to the Braj region by providing verified, real-time guidance through the most widely used messaging platform in India.

---

## SECTION 9: BRIEF DESCRIPTION OF DRAWINGS

**Figure 1:** System Architecture Diagram — End-to-end flow from WhatsApp user to database and back.

**Figure 2:** Registry-Based FSM State Transition Graph — All 7 states and their transitions.

**Figure 3:** Three-Tier Schedule Resolution Algorithm — Festival override → Seasonal → General.

**Figure 4:** Persistent Session Context Data Model — UserSession table + SessionContext JSON schema.

**Figure 5:** Database Entity-Relationship Diagram — All 12 tables and their relationships.

**Figure 6:** Multilingual Translation Architecture — JSON translation file + column-per-language DB model.

**Figure 7:** Webhook Security Flow — HMAC-SHA1 validation sequence diagram.

---

## SECTION 10: INDUSTRIAL APPLICABILITY

BrajPath is directly applicable to:

1. **Religious Tourism** — Any pilgrimage destination globally (Varanasi, Tirupati, Amritsar, Mecca, Vatican, etc.)
2. **Cultural Heritage Sites** — Museums, monuments, UNESCO World Heritage Sites
3. **Event Management** — Festival guidance systems (Kumbh Mela, Pushkar Fair)
4. **Smart City Infrastructure** — Municipal information systems via WhatsApp
5. **Healthcare Navigation** — Hospital guidance systems for rural populations
6. **Government Services** — Citizen service delivery via messaging platforms

The WhatsApp-first approach is particularly applicable in markets with high messaging app penetration and lower smartphone app adoption rates.

---

## SECTION 11: PRIOR ART DIFFERENTIATION

| Feature | BrajPath | Generic Chatbots | Temple Websites | Google Maps |
|---------|----------|-----------------|-----------------|-------------|
| WhatsApp-native | ✅ | Partial | ❌ | ❌ |
| Multilingual (4 langs) | ✅ | Partial | ❌ | Partial |
| Seasonal timing logic | ✅ | ❌ | ❌ | ❌ |
| Festival overrides | ✅ | ❌ | ❌ | ❌ |
| Bhog period modeling | ✅ | ❌ | ❌ | ❌ |
| Persistent context | ✅ | Partial | ❌ | ❌ |
| Community fare guide | ✅ | ❌ | ❌ | ❌ |
| Registry-based FSM | ✅ | ❌ | N/A | N/A |
| Analytics logging | ✅ | Partial | ❌ | N/A |
| No app install needed | ✅ | Partial | ❌ | ❌ |

---

## SECTION 12: SOURCE CODE REFERENCE

The complete source code is maintained at:
**https://github.com/Mradulmanimishra/BrajPath**

### Key Files for Patent Reference:

| File | Patent Relevance |
|------|-----------------|
| `app/services/state_machine.py` | Registry-Based FSM (Claims 1, 2, 9) |
| `app/services/context_service.py` | Session Context Engine (Claims 1, 3) |
| `app/services/temple_service.py` | Timing Engine, Translation, Routes (Claims 1, 4, 5, 6) |
| `app/api/webhook.py` | Secure Gateway (Claims 1, 8) |
| `app/db/models.py` | Database Schema (Claims 1, 5, 7) |
| `app/db/session.py` | Database Connection Management |
| `app/services/timezone_utils.py` | IST/UTC Timezone Handling |
| `app/config.py` | Environment Configuration |
| `app/main.py` | Application Lifecycle Management |

---

## SECTION 13: VERSION HISTORY

| Version | Date | Key Changes |
|---------|------|-------------|
| 1.0.0 | April 2026 | Initial release — Core FSM, multilingual support, temple timings, routes |

---

## SECTION 14: GLOSSARY

| Term | Definition |
|------|-----------|
| FSM | Finite State Machine — A computational model with a finite number of states and defined transitions |
| Handler Registry | A dictionary mapping state names to handler functions, populated at module load time |
| Context Engine | System for storing and retrieving user behavioral history across sessions |
| Bhog Period | Midday ritual closure period in Vaishnava temples during which the deity is offered food |
| TwiML | Twilio Markup Language — XML format for WhatsApp/SMS responses |
| IST | Indian Standard Time — UTC+5:30 |
| E.164 | International telephone numbering format (e.g., +919876543210) |
| HMAC-SHA1 | Hash-based Message Authentication Code using SHA-1 — used for webhook signature validation |
| ORM | Object-Relational Mapper — SQLAlchemy in this system |
| Pending Action | A cross-state context field that preserves user intent across multiple conversation turns |
| Seasonal Schedule | Temple timing schedule specific to a season (summer/winter/monsoon) |
| Festival Override | A date-range based schedule that supersedes seasonal schedules during Hindu festivals |

---

*Document prepared for patent filing purposes.*
*All technical details are based on the actual implemented source code.*
*GitHub Repository: https://github.com/Mradulmanimishra/BrajPath*
*Date: April 2026*
