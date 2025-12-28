# Frontend API Integration Fix

## Issue

When clicking "Select a Chord to Reharmonize" in the frontend, nothing happens.

## Root Cause

The frontend service (`chordService.ts`) was using inconsistent trailing slashes in API endpoint URLs, which caused issues with FastAPI's routing.

## FastAPI Trailing Slash Behavior

FastAPI has specific rules for trailing slashes:

1. **List/Collection Endpoints** - Use trailing slash: `/chords/`
2. **Item/Detail Endpoints with Path Parameters** - No trailing slash: `/chords/{symbol}`
3. **Action Endpoints with Path Parameters** - No trailing slash: `/reharmonize/substitutions/{chord}`

### Why This Matters

When you call an endpoint without the correct trailing slash format:
- FastAPI issues a 307 Temporary Redirect
- Axios in the browser follows the redirect automatically
- BUT: The redirect can cause issues with:
  - Request timing
  - Error handling
  - Browser DevTools showing two requests instead of one

## Solution

Updated `frontend/src/services/chordService.ts` with correct trailing slash usage:

```typescript
export const chordService = {
  // ✓ List endpoint - WITH trailing slash
  async getChords(): Promise<Chord[]> {
    const response = await apiClient.get('/chords/');
    return response.data;
  },

  // ✓ Path parameter endpoints - NO trailing slash
  async getChord(symbol: string): Promise<Chord> {
    const response = await apiClient.get(`/chords/${symbol}`);
    return response.data;
  },

  async getChordsByKey(keySignature: string): Promise<Chord[]> {
    const response = await apiClient.get(`/keys/${keySignature}/chords`);
    return response.data;
  },

  async getSubstitutions(
    chordSymbol: string,
    technique: string = 'random'
  ): Promise<SubstitutionResponse> {
    const response = await apiClient.get(
      `/reharmonize/substitutions/${chordSymbol}`,
      { params: { technique } }
    );
    return response.data;
  },

  async getImprovisationNotes(
    chordSymbol: string,
    count: number = 5
  ): Promise<ImprovisationNotesResponse> {
    const response = await apiClient.get(
      `/improvisation/notes/${chordSymbol}`,
      { params: { count } }
    );
    return response.data;
  },
};
```

## Endpoint Reference

| Endpoint | Correct Format | Trailing Slash? |
|----------|---------------|----------------|
| Get all chords | `/chords/` | ✓ Yes |
| Get one chord | `/chords/{symbol}` | ✗ No |
| Get chord notes | `/chords/{symbol}/notes` | ✗ No |
| Get chord extensions | `/chords/{symbol}/extensions` | ✗ No |
| Get all keys | `/keys/` | ✓ Yes |
| Get one key | `/keys/{key_name}` | ✗ No |
| Get key chords | `/keys/{key_name}/chords` | ✗ No |
| Get substitutions | `/reharmonize/substitutions/{chord}` | ✗ No |
| Analyze substitutions | `/reharmonize/substitutions/analyze` | ✗ No |
| Get improvisation notes | `/improvisation/notes/{chord}` | ✗ No |

## Additional Improvements

### Enhanced Error Logging

Updated `frontend/src/services/api.ts` with better error logging:

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    } else if (error.request) {
      console.error('No response received:', error.request);
    } else {
      console.error('Error message:', error.message);
    }
    return Promise.reject(error);
  }
);
```

### Redirect Configuration

Added explicit redirect configuration to axios:

```typescript
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  maxRedirects: 5, // Explicitly allow redirects
});
```

## Testing

After these fixes, the frontend should:

1. ✓ Load chords successfully when entering chord list
2. ✓ Display chord buttons in "Select a Chord to Reharmonize" section
3. ✓ Show substitutions when clicking a chord
4. ✓ Display improvisation notes
5. ✓ Show music notation for all chords and notes

## Debugging

If the frontend still doesn't work:

1. **Check Browser Console** (F12)
   - Look for "API Error:" messages
   - Check Network tab for failed requests
   - Verify no CORS errors

2. **Check Backend Logs**
   ```bash
   docker-compose logs backend | grep ERROR
   ```

3. **Test API Directly**
   ```bash
   # Should work
   curl "http://localhost:8000/api/v1/chords/"

   # Should redirect (307) then work
   curl -L "http://localhost:8000/api/v1/chords"

   # Should work
   curl "http://localhost:8000/api/v1/reharmonize/substitutions/C?technique=random"
   ```

4. **Verify Frontend Environment**
   ```bash
   docker-compose logs frontend | grep ERROR
   ```

5. **Check CORS Configuration**
   Backend `.env` should have:
   ```
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000
   ```

## Common Issues

### Issue: CORS Error
**Symptom:** Browser console shows "Access-Control-Allow-Origin" error
**Fix:** Verify backend CORS_ORIGINS includes `http://localhost:5173`

### Issue: Network Error
**Symptom:** "Network Error" in console
**Fix:** Ensure backend is running: `docker-compose ps backend`

### Issue: 404 Not Found
**Symptom:** API returns 404
**Fix:** Check endpoint URL matches backend routes exactly

### Issue: Empty Response
**Symptom:** API returns 200 but no data
**Fix:** Check database has data: `curl http://localhost:8000/api/v1/chords/`

## Files Changed

1. `frontend/src/services/chordService.ts` - Fixed trailing slashes
2. `frontend/src/services/api.ts` - Enhanced error logging and redirect config

## Testing Checklist

- [ ] Frontend loads without errors
- [ ] Can enter chords in "Modern Music" mode
- [ ] Chord buttons appear in "Select a Chord" section
- [ ] Clicking a chord shows loading spinner
- [ ] Substitutions appear with music notation
- [ ] Improvisation notes appear below
- [ ] No console errors in browser
- [ ] Network tab shows successful API calls
