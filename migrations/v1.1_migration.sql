-- v1.1 migration — non-breaking additive columns 
-- Run ONCE before restarting the FastAPI server. 
   
 ALTER TABLE user_sessions 
     ADD COLUMN IF NOT EXISTS pending_action VARCHAR(20) DEFAULT NULL, 
     ADD COLUMN IF NOT EXISTS selected_area  VARCHAR(50) DEFAULT NULL; 
   
 COMMENT ON COLUMN user_sessions.pending_action IS 
     'Stores which flow triggered area-select: timing | route | advisory'; 
 COMMENT ON COLUMN user_sessions.selected_area IS 
     'Stores chosen area code: vrindavan | mathura | govardhan | outstation'; 
