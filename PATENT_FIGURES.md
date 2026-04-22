# PATENT FIGURES — BrajPath
## Section 9: Complete Drawing Descriptions for All 7 Figures
### Tools: Napkin AI (napkin.ai) + GPAI (Gemini / Imagen)

---

## HOW TO USE THIS DOCUMENT

- **Napkin AI** → Best for flowcharts, architecture diagrams, state machines, ER diagrams
  - Go to: https://www.napkin.ai
  - Paste the "NAPKIN AI PROMPT" text directly into Napkin AI
  - It auto-generates a professional diagram

- **GPAI (Google Gemini / Imagen)** → Best for visual illustrations, infographics, system overview art
  - Go to: https://gemini.google.com or https://labs.google/fx/tools/image-fx
  - Use the "GPAI PROMPT" for image generation

---

---

# FIGURE 1
## System Architecture Diagram
### "End-to-End Flow from WhatsApp User to Database and Back"

---

### WHAT THIS FIGURE SHOWS:
The complete system architecture of BrajPath showing how a message travels from a pilgrim's WhatsApp phone through Twilio, FastAPI, the State Machine, Temple Service, and finally to the PostgreSQL/SQLite database — and the response path back.

---

### NAPKIN AI PROMPT (Copy-Paste This):

```
Create a vertical system architecture flowchart for a WhatsApp chatbot system called BrajPath with the following layers connected by arrows:

TOP LAYER (User):
- Box: "Pilgrim (User)" with icon of mobile phone
- Label: "WhatsApp Mobile App"
- Arrow DOWN labeled "WhatsApp Message (text)"

LAYER 2 (External Gateway):
- Box: "Twilio API Gateway"
- Sub-label: "HMAC-SHA1 Signature Validation"
- Arrow DOWN labeled "HTTP POST /whatsapp/webhook"

LAYER 3 (Web Server):
- Box: "FastAPI Async Webhook Layer"
- 3 bullet points inside: "Phone Validation (E.164)", "Request Authentication", "TwiML Response Formatter"
- Arrow DOWN labeled "Validated Request"

LAYER 4 (Core Engine) — use a dashed border box containing:
- Left box: "Handler Registry (dict)" connected by arrow to right box: "State Handlers (7 states)"
- Below those: "Context Manager (Session JSON)"
- Label this group: "Registry-Based State Machine Engine"
- Arrow DOWN labeled "Service Call"

LAYER 5 (Service):
- Box: "Temple Service Layer"
- 4 bullet points: "Seasonal Timing Engine", "Route & Fare Calculator", "Advisory Formatter", "Translation Loader"
- Arrow DOWN labeled "SQL Query"

LAYER 6 (Database):
- Box: "Persistence Layer (SQLAlchemy ORM)"
- Show 3 sub-boxes side by side: "temples / schedules / routes", "user_sessions / query_logs", "partners / advisories"

Add a return arrow on the RIGHT SIDE going UP from Database back to User labeled "TwiML XML Response → WhatsApp Reply"

Color scheme: Blue for user layer, Orange for gateway, Green for web server, Purple for state machine, Teal for service, Gray for database.
```

---

### GPAI PROMPT (For Illustrated Version):

```
Create a clean, professional technical architecture diagram for a patent application. 
Show a vertical flowchart with 6 layers connected by arrows:
1. Top: A smartphone showing WhatsApp interface (pilgrim user)
2. Twilio cloud gateway with security shield icon
3. FastAPI server box with Python logo
4. A central engine box with gear icons showing "State Machine" and "Context Manager"
5. A service layer box with temple/building icons
6. Bottom: Database cylinders labeled PostgreSQL and SQLite

Use a blue and white color scheme with subtle gradient. 
Add directional arrows between each layer. 
Include small icons: lock icon on Twilio, gear on state machine, database cylinder at bottom.
Style: Clean, minimal, suitable for patent filing. White background. Professional technical illustration.
No text labels needed — just the visual structure.
```

---

### FIGURE CAPTION (For Patent Filing):
**FIG. 1** — System Architecture of BrajPath showing the end-to-end message processing pipeline from WhatsApp user input through the Twilio API Gateway, FastAPI Webhook Layer, Registry-Based State Machine Engine, Temple Service Layer, and Persistence Layer, with the response path returning as TwiML XML.

---

---

# FIGURE 2
## Registry-Based FSM State Transition Graph
### "All 7 States and Their Transitions"

---

### WHAT THIS FIGURE SHOWS:
A state diagram showing all 7 conversation states in BrajPath and every possible transition between them, including entry triggers, back navigation, and terminal states.

---

### NAPKIN AI PROMPT (Copy-Paste This):

```
Create a state machine diagram (finite state machine / FSM) with the following states and transitions:

STATES (draw as rounded rectangles):
1. [START] — initial pseudo-state (filled circle)
2. language_select — "Language Selection"
3. main_menu — "Main Menu (7 options)"
4. temple_area_select — "Select Area (Vrindavan/Mathura/Govardhan/Outstation)"
5. area_temple_select — "Select Temple"
6. route_from_select — "Select Starting Point"
7. partner_category_select — "Select Partner Category"
8. partner_list — "View Partners"

TRANSITIONS (draw as labeled arrows):
- [START] → language_select : "New user / first message"
- ANY STATE → main_menu : "Entry trigger (hello/hi/menu/start/hare krishna)"
- language_select → main_menu : "Valid language choice (1/2/3/4)"
- language_select → language_select : "Invalid input (loop)"
- main_menu → temple_area_select : "Choice 2 (timings) / pending=timing"
- main_menu → temple_area_select : "Choice 3 (routes) / pending=route"
- main_menu → temple_area_select : "Choice 6 (advisory) / pending=advisory"
- main_menu → partner_category_select : "Choice 5 (partners)"
- main_menu → language_select : "Choice 7 (change language)"
- main_menu → main_menu : "Choice 0 (resend menu)"
- temple_area_select → area_temple_select : "Valid area selected"
- temple_area_select → main_menu : "Choice 0 (back)"
- area_temple_select → main_menu : "Timing shown / Advisory shown"
- area_temple_select → route_from_select : "pending=route"
- area_temple_select → temple_area_select : "Choice 0 (back)"
- route_from_select → main_menu : "Route shown"
- route_from_select → temple_area_select : "Choice 0 (back)"
- partner_category_select → partner_list : "Valid category selected"
- partner_category_select → main_menu : "Choice 0 (back)"
- partner_list → partner_category_select : "Choice 0 (back)"
- partner_list → main_menu : "Other input"

Mark main_menu as the central hub state with double border.
Use different colors: Blue=menu states, Green=temple states, Orange=route states, Purple=partner states.
Add a legend in the corner.
```

---

### GPAI PROMPT (For Illustrated Version):

```
Create a clean state machine diagram for a patent application showing conversation flow states.
Draw 8 rounded rectangle boxes connected by curved arrows with labels.
Central box labeled "Main Menu" should be larger and highlighted in blue.
Surrounding boxes: "Language Select" (top), "Area Select" (left), "Temple Select" (bottom-left), "Route Select" (bottom), "Partner Category" (right), "Partner List" (far right).
Show arrows between boxes with small text labels on arrows.
Use pastel colors: blue for menu, green for temple flow, orange for route flow, purple for partner flow.
White background, clean minimal style suitable for patent filing.
Include a small legend box in the corner.
Professional technical diagram style.
```

---

### FIGURE CAPTION (For Patent Filing):
**FIG. 2** — State Transition Diagram of the Registry-Based Finite State Machine showing all 7 conversation states (language_select, main_menu, temple_area_select, area_temple_select, route_from_select, partner_category_select, partner_list) and their valid transitions, including entry triggers, back navigation paths, and the central main_menu hub state.

---

---

# FIGURE 3
## Three-Tier Schedule Resolution Algorithm
### "Festival Override → Seasonal → General"

---

### WHAT THIS FIGURE SHOWS:
A decision flowchart showing how BrajPath determines which temple schedule to display, using a priority-based three-tier resolution system.

---

### NAPKIN AI PROMPT (Copy-Paste This):

```
Create a decision flowchart (top to bottom) for a temple schedule resolution algorithm:

TITLE: "Three-Tier Temple Schedule Resolution Algorithm"

START: Diamond shape "Query: Get Active Schedule for Temple X on Date D"

TIER 1 (Red/Priority 1):
→ Process box: "Check festival_overrides table WHERE date_from ≤ D ≤ date_to AND is_active = TRUE"
→ Diamond: "Festival Override Found?"
→ YES arrow → Box: "USE FESTIVAL OVERRIDE SCHEDULE" (Red box, labeled "Priority 1: Festival Override")
→ NO arrow → Continue to Tier 2

TIER 2 (Orange/Priority 2):
→ Process box: "Detect Current Season: month 11,12,1,2 = winter | month 7,8,9,10 = monsoon | else = summer"
→ Process box: "Check schedules table WHERE season = [current_season] AND is_current = TRUE"
→ Diamond: "Seasonal Schedule Found?"
→ YES arrow → Box: "USE SEASONAL SCHEDULE" (Orange box, labeled "Priority 2: Seasonal Schedule")
→ NO arrow → Continue to Tier 3

TIER 3 (Green/Priority 3):
→ Process box: "Check schedules table WHERE season = 'general' AND is_current = TRUE"
→ Diamond: "General Schedule Found?"
→ YES arrow → Box: "USE GENERAL SCHEDULE" (Green box, labeled "Priority 3: General Fallback")
→ NO arrow → Box: "RETURN: Timing information not available" (Gray box)

FINAL STEP (after any schedule is found):
→ Box: "Apply Open/Closed Logic: Check morning window + evening window - bhog period"
→ Box: "Return Formatted Timing Card to User"

Add a note box: "Bhog Period = Midday ritual closure unique to Vaishnava temples"
Color code: Red=Festival, Orange=Seasonal, Green=General, Gray=Not found
```

---

### GPAI PROMPT (For Illustrated Version):

```
Create a vertical decision flowchart diagram for a patent application.
Show 3 tiers of decision boxes connected by YES/NO arrows:

Tier 1 (top, red): "Festival Override Check" — diamond decision box
Tier 2 (middle, orange): "Seasonal Schedule Check" — diamond decision box  
Tier 3 (bottom, green): "General Schedule Fallback" — diamond decision box

Each tier has a YES path going right to a colored result box.
NO paths continue downward to the next tier.
At the very bottom: a gray "Not Available" box.

After any result box, show an arrow going to a final blue box: "Calculate Open/Closed Status"

Include small calendar icons on tier 1, sun/snowflake icons on tier 2, and a generic clock on tier 3.
White background, clean professional style for patent filing.
Add a small legend showing the 3 priority levels with their colors.
```

---

### FIGURE CAPTION (For Patent Filing):
**FIG. 3** — Three-Tier Temple Schedule Resolution Algorithm showing the priority-based decision flow: (1) Festival Override check using date-range matching, (2) Seasonal Schedule selection based on current month classification (summer/winter/monsoon), and (3) General Schedule fallback, followed by real-time open/closed status calculation incorporating the Bhog midday closure period.

---

---

# FIGURE 4
## Persistent Session Context Data Model
### "UserSession Table + SessionContext JSON Schema"

---

### WHAT THIS FIGURE SHOWS:
A combined diagram showing the relational database schema of the UserSession table alongside the JSON structure of the SessionContext Pydantic model stored in the context_data column.

---

### NAPKIN AI PROMPT (Copy-Paste This):

```
Create a data model diagram showing two connected components:

LEFT SIDE — Database Table (draw as a UML class diagram / table):
Title: "user_sessions (SQL Table)"
Columns (show as rows with type):
  id              INTEGER  PRIMARY KEY
  wa_number       VARCHAR(30)  UNIQUE  ← "WhatsApp Identifier"
  language_code   VARCHAR(10)          ← "en/hi/bn/ta"
  current_state   VARCHAR(60)          ← "FSM Current State"
  prev_state      VARCHAR(60)          ← "Previous State"
  selected_temple VARCHAR(60)          ← "Active Temple Context"
  selected_area   VARCHAR(50)          ← "Active Area Context"
  selected_route_from VARCHAR(60)      ← "Route Origin"
  pending_action  VARCHAR(20)          ← "Cross-State Intent"
  context_data    TEXT                 ← "JSON Blob ↓" (highlighted in yellow)
  message_count   INTEGER              ← "Engagement Metric"
  last_seen_at    DATETIME             ← "Activity Timestamp"
  created_at      DATETIME

RIGHT SIDE — JSON Schema (draw as a nested box structure):
Title: "SessionContext (JSON in context_data)"
Show as nested boxes:
{
  "last_visited_area": "vrindavan",        ← string
  "last_visited_temple": "banke_bihari",   ← string
  "preferred_city": "Vrindavan",           ← string
  "interaction_history": [                 ← array (sliding window, max 10)
    "entry_trigger",
    "timing_select",
    "set_language"
  ],
  "metadata": {}                           ← dict for future use
}

Connect the context_data column on the left to the JSON box on the right with a dashed arrow labeled "Serialized as JSON string"

Add a note: "Sliding window: max 10 interactions stored"
Add a note: "pending_action enables cross-state intent propagation"

Color: Blue for SQL table, Yellow highlight for context_data column, Green for JSON structure
```

---

### GPAI PROMPT (For Illustrated Version):

```
Create a technical data model diagram for a patent application showing two connected components side by side.

LEFT: A database table diagram with column names and data types listed in rows. 
Highlight one row labeled "context_data TEXT" in yellow.
Title: "UserSession Database Table"

RIGHT: A JSON structure diagram showing nested key-value pairs in a code-style box.
Show keys: last_visited_area, last_visited_temple, interaction_history (as array), metadata.
Title: "SessionContext JSON Schema"

Connect the highlighted "context_data" row to the JSON box with a dashed arrow.

Use blue for the database table, green for the JSON box, yellow for the highlighted connection field.
White background, clean minimal style for patent filing.
Add small icons: database cylinder icon on left, curly braces {} icon on right.
Professional technical diagram style.
```

---

### FIGURE CAPTION (For Patent Filing):
**FIG. 4** — Persistent Session Context Data Model showing the UserSession relational table schema (left) and the SessionContext JSON structure stored in the context_data column (right). The context_data field stores a serialized Pydantic model containing geospatial history, a sliding-window interaction history (maximum 10 entries), and extensible metadata. The pending_action field enables cross-state intent propagation across multiple conversation turns.

---

---

# FIGURE 5
## Database Entity-Relationship Diagram
### "All 12 Tables and Their Relationships"

---

### WHAT THIS FIGURE SHOWS:
A complete ER diagram of all 12 database tables in BrajPath, showing primary keys, foreign keys, and relationships between entities.

---

### NAPKIN AI PROMPT (Copy-Paste This):

```
Create a database Entity-Relationship (ER) diagram with the following 12 tables and relationships:

CORE TEMPLE GROUP (center, blue):
Table: temples
  PK: id
  Fields: code, name_en, name_hi, name_bn, name_ta, area, city, latitude, longitude, is_active

Table: schedules
  PK: id
  FK: temple_id → temples.id
  Fields: season, open_morning, close_morning, bhog_start, bhog_end, open_evening, close_evening, is_current

Table: festival_overrides
  PK: id
  FK: temple_id → temples.id
  Fields: festival_name, date_from, date_to, open_morning, open_evening, is_active

Table: temple_advisories
  PK: id
  FK: temple_id → temples.id
  Fields: advisory_type, message_en, message_hi, message_bn, message_ta, priority, is_active

ROUTING GROUP (left, green):
Table: route_points
  PK: id
  Fields: code, name_en, point_type, latitude, longitude

Table: routes
  PK: id
  FK: from_point_id → route_points.id
  FK: temple_id → temples.id
  Fields: mode, duration_min_est, fare_min, fare_max, route_text_en, is_active

Table: fare_guides
  PK: id
  Fields: from_label, to_label, service_type, fare_min, fare_max

PARTNER GROUP (right, orange):
Table: partner_categories
  PK: id
  Fields: code, name, icon_emoji, priority_order

Table: partners
  PK: id
  FK: category_id → partner_categories.id
  Fields: name, phone, whatsapp, area, is_active

USER & ANALYTICS GROUP (bottom, purple):
Table: user_sessions
  PK: id
  Fields: wa_number, language_code, current_state, context_data, message_count

Table: support_requests
  PK: id
  FK: temple_id → temples.id
  Fields: wa_number, request_type, message_text, status

Table: query_logs
  PK: id
  Fields: wa_number, detected_state, detected_intent, response_status, created_at

RELATIONSHIPS (draw as lines with crow's foot notation):
- temples ||--o{ schedules (one temple has many schedules)
- temples ||--o{ festival_overrides (one temple has many overrides)
- temples ||--o{ temple_advisories (one temple has many advisories)
- temples ||--o{ routes (one temple has many routes)
- route_points ||--o{ routes (one point has many routes)
- partner_categories ||--o{ partners (one category has many partners)
- temples ||--o{ support_requests (one temple has many support requests)

Color groups: Blue=temple core, Green=routing, Orange=partners, Purple=user/analytics
```

---

### GPAI PROMPT (For Illustrated Version):

```
Create a clean database entity-relationship diagram for a patent application.
Show 12 rectangular table boxes arranged in 4 color-coded groups:

Blue group (center): temples, schedules, festival_overrides, temple_advisories
Green group (left): route_points, routes, fare_guides
Orange group (right): partner_categories, partners
Purple group (bottom): user_sessions, support_requests, query_logs

Each box shows the table name at top and 3-4 key field names below.
Connect related tables with lines showing one-to-many relationships (crow's foot notation).
The "temples" table should be the largest, central box with the most connections.

White background, clean grid layout, professional style for patent filing.
Add a small legend showing the 4 color groups and their purposes.
```

---

### FIGURE CAPTION (For Patent Filing):
**FIG. 5** — Entity-Relationship Diagram of the BrajPath persistence layer showing all 12 normalized database tables organized into four functional groups: Temple Core (temples, schedules, festival_overrides, temple_advisories), Routing (route_points, routes, fare_guides), Partner Directory (partner_categories, partners), and User/Analytics (user_sessions, support_requests, query_logs). Foreign key relationships are shown with crow's foot notation.

---

---

# FIGURE 6
## Multilingual Translation Architecture
### "JSON Translation File + Column-Per-Language DB Model"

---

### WHAT THIS FIGURE SHOWS:
A diagram showing the two-layer multilingual architecture: the JSON translation file for UI strings and the column-per-language database model for content data.

---

### NAPKIN AI PROMPT (Copy-Paste This):

```
Create a multilingual architecture diagram with two main sections:

SECTION A — LEFT SIDE: "Layer 1: UI String Translations (JSON File)"
Show a JSON file structure:
translations.json
{
  "welcome": {
    "en": "Welcome to BrajPath...",
    "hi": "BrajPath में आपका स्वागत है...",
    "bn": "BrajPath-এ আপনাকে স্বাগতম...",
    "ta": "BrajPath-ல் உங்களை வரவேற்கிறோம்..."
  },
  "main_menu": { "en": "...", "hi": "...", "bn": "...", "ta": "..." },
  "select_area": { "en": "...", "hi": "...", "bn": "...", "ta": "..." }
}

Show a function box below:
tr(key, lang) → Lazy-loaded, cached, fallback to English

SECTION B — RIGHT SIDE: "Layer 2: Content Translations (Database Columns)"
Show a table with column-per-language pattern:

temples table:
  name_en | name_hi | name_bn | name_ta
  "Shri Banke Bihari Mandir" | "श्री बांके बिहारी मंदिर" | "শ্রী বাঁকে বিহারী মন্দির" | "ஸ்ரீ பாங்கே பிஹாரி மந்திர்"

routes table:
  route_text_en | route_text_hi | route_text_bn | route_text_ta

temple_advisories table:
  message_en | message_hi | message_bn | message_ta

SECTION C — BOTTOM: "Language Selection Flow"
Show 4 flag/language boxes:
[1. English 🇬🇧] [2. हिंदी 🇮🇳] [3. বাংলা 🇧🇩] [4. தமிழ் 🇮🇳]
Arrow: "User selects → stored in user_sessions.language_code → used in all tr() calls"

Add a note: "O(1) retrieval — no JOIN needed for language lookup"
Add a note: "Fallback chain: requested lang → English → [key]"

Color: Blue=JSON layer, Green=Database layer, Orange=Language selection
```

---

### GPAI PROMPT (For Illustrated Version):

```
Create a multilingual architecture diagram for a patent application showing two parallel systems.

LEFT SIDE: A JSON file icon with nested key-value pairs showing the same text in 4 languages (English, Hindi, Bengali, Tamil). Show 4 colored language tags: blue=English, saffron=Hindi, green=Bengali, red=Tamil.

RIGHT SIDE: A database table showing 4 parallel columns, each with a language flag icon at the top (English, Hindi, Bengali, Tamil). Show sample text in each column.

CENTER: A function box labeled "tr(key, lang)" with arrows from both sides pointing to it.

BOTTOM: 4 language selection buttons showing: "1. English", "2. हिंदी", "3. বাংলা", "4. தமிழ்"

Use the 4 language colors consistently throughout.
White background, clean professional style for patent filing.
Add a small note: "Graceful fallback to English if translation missing"
```

---

### FIGURE CAPTION (For Patent Filing):
**FIG. 6** — Multilingual Translation Architecture showing the two-layer approach: Layer 1 uses a lazy-loaded JSON translation file for UI strings with a tr(key, lang) function providing graceful English fallback; Layer 2 uses a column-per-language relational storage model (name_en, name_hi, name_bn, name_ta) for content data, enabling O(1) language-specific retrieval without JOIN operations. The system supports English, Hindi, Bengali, and Tamil, with the user's language preference persisted in the user_sessions table.

---

---

# FIGURE 7
## Webhook Security Flow
### "HMAC-SHA1 Validation Sequence Diagram"

---

### WHAT THIS FIGURE SHOWS:
A UML sequence diagram showing the complete security validation flow when a WhatsApp message arrives, including HMAC-SHA1 signature verification, phone number validation, and the response path.

---

### NAPKIN AI PROMPT (Copy-Paste This):

```
Create a UML sequence diagram with the following participants (left to right):
1. Pilgrim (WhatsApp User)
2. Twilio (API Gateway)
3. BrajPath Webhook (FastAPI)
4. Validator (HMAC-SHA1)
5. State Machine
6. Database

SEQUENCE OF MESSAGES (draw as horizontal arrows with labels):

1. Pilgrim → Twilio: "Sends WhatsApp message: 'hello'"
2. Twilio → BrajPath Webhook: "HTTP POST /whatsapp/webhook\nHeaders: X-Twilio-Signature: [HMAC-SHA1 hash]\nBody: From=whatsapp:+91xxx, Body=hello"
3. BrajPath Webhook → Validator: "validate(url, form_data, signature)"
4. Validator → Validator: "Compute HMAC-SHA1(auth_token, url+params)"

DECISION POINT (add an alt/else box):
  [IF signature INVALID]:
    Validator → BrajPath Webhook: "Return: False"
    BrajPath Webhook → Twilio: "HTTP 403 Forbidden"
    Twilio → Pilgrim: "No response (message dropped)"
  
  [IF signature VALID]:
    Validator → BrajPath Webhook: "Return: True"
    BrajPath Webhook → BrajPath Webhook: "Validate phone number (E.164 regex)"
    BrajPath Webhook → State Machine: "process_message(wa_number, text, db)"
    State Machine → Database: "SELECT user_session WHERE wa_number=?"
    Database → State Machine: "Return UserSession"
    State Machine → State Machine: "Dispatch to registered handler"
    State Machine → Database: "UPDATE user_session + INSERT query_log"
    State Machine → BrajPath Webhook: "Return reply_text"
    BrajPath Webhook → Twilio: "HTTP 200 OK\nTwiML XML Response"
    Twilio → Pilgrim: "WhatsApp Reply Message"

Add timing note: "Total processing: typically < 200ms"
Add security note: "HMAC-SHA1 prevents message spoofing from non-Twilio sources"
Color: Red=security checks, Green=success path, Blue=normal flow
```

---

### GPAI PROMPT (For Illustrated Version):

```
Create a UML sequence diagram for a patent application showing a security validation flow.

Show 6 vertical lifelines (columns) labeled:
1. "User (WhatsApp)" — with phone icon
2. "Twilio Gateway" — with cloud icon
3. "FastAPI Webhook" — with server icon
4. "HMAC Validator" — with lock/shield icon
5. "State Machine" — with gear icon
6. "Database" — with cylinder icon

Show horizontal arrows between lifelines representing message flow.
Include a red highlighted box showing the "INVALID SIGNATURE → 403 Forbidden" rejection path.
Include a green highlighted box showing the "VALID → Process Message" success path.

Add a small security badge icon near the HMAC Validator.
White background, clean professional style for patent filing.
Use red for security rejection path, green for success path, blue for normal flow.
```

---

### FIGURE CAPTION (For Patent Filing):
**FIG. 7** — Webhook Security Sequence Diagram showing the HMAC-SHA1 cryptographic validation flow. Incoming HTTP POST requests from Twilio include an X-Twilio-Signature header containing an HMAC-SHA1 hash of the request URL and form parameters signed with the Twilio Auth Token. The BrajPath validator recomputes this hash and rejects requests with mismatched signatures with HTTP 403 Forbidden, preventing message spoofing. Valid requests proceed through phone number validation (E.164 regex), state machine dispatch, database operations, and TwiML XML response generation.

---

---

# SUMMARY TABLE — All 7 Figures

| Figure | Title | Best Tool | Type |
|--------|-------|-----------|------|
| FIG. 1 | System Architecture | Napkin AI | Layered Architecture |
| FIG. 2 | FSM State Transitions | Napkin AI | State Machine Diagram |
| FIG. 3 | Schedule Resolution Algorithm | Napkin AI | Decision Flowchart |
| FIG. 4 | Session Context Data Model | Napkin AI | Data Model Diagram |
| FIG. 5 | Database ER Diagram | Napkin AI | ER Diagram |
| FIG. 6 | Multilingual Architecture | Napkin AI + GPAI | Architecture Diagram |
| FIG. 7 | Webhook Security Flow | Napkin AI | Sequence Diagram |

---

# STEP-BY-STEP INSTRUCTIONS

## Using Napkin AI (Recommended for all 7 figures):

1. Go to **https://www.napkin.ai**
2. Create a new document
3. Copy the "NAPKIN AI PROMPT" text for the figure you want
4. Paste it into Napkin AI's text area
5. Click "Generate Diagram"
6. Download as SVG or PNG
7. Label it as FIG. 1, FIG. 2, etc.

## Using GPAI / Google Imagen:

1. Go to **https://labs.google/fx/tools/image-fx**
   OR use **https://gemini.google.com** (Gemini Advanced)
2. Copy the "GPAI PROMPT" text
3. Paste into the image generation field
4. Generate and download
5. Use as supplementary visual for the patent

## For Patent Filing (Indian Patent Office):

- Save all figures as **PDF or TIFF** format
- Minimum resolution: **300 DPI**
- Black and white versions also required
- Label each figure: **"FIG. 1", "FIG. 2"** etc.
- Each figure must fit on an **A4 page**
- Submit with the patent application as **Form 3 (Statement and Undertaking)**

---

# PATENT FIGURE CHECKLIST

- [ ] FIG. 1 — System Architecture Diagram ✅ Prompt Ready
- [ ] FIG. 2 — FSM State Transition Graph ✅ Prompt Ready
- [ ] FIG. 3 — Schedule Resolution Algorithm ✅ Prompt Ready
- [ ] FIG. 4 — Session Context Data Model ✅ Prompt Ready
- [ ] FIG. 5 — Database ER Diagram ✅ Prompt Ready
- [ ] FIG. 6 — Multilingual Architecture ✅ Prompt Ready
- [ ] FIG. 7 — Webhook Security Flow ✅ Prompt Ready

---

*All prompts are based on the actual implemented source code of BrajPath.*
*GitHub: https://github.com/Mradulmanimishra/BrajPath*
*For patent filing with Indian Patent Office (IPO) under The Patents Act, 1970*
