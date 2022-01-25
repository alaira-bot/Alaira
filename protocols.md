# Database communication
## Request
```json5
{
  "id": 12345, // message ID
  "op": "opcode",
  // other data here
}
```
## Response
```json5
{
  "id": 12345, // request ID
  "status": 200, // HTTP status codes or custom codes are allowed here
  // other data here
}
```
Note: responses **must** return a status. Alaira will issue a warning otherwise.
## Example
### Request
```json5
{
  "id": 14,
  "op": "ping"
}
```
### Response
```json5
{
  "id": 14,
  "status": 200 // OK
}
```
## Callbacks
Callbacks are defined in `database/routes`. The file is imported and the 
file's `setup` function is called, with the only argument being the route 
callback table. Each callback takes two arguments - the opcode, and the 
payload stripped of `id` and `op` keys.
### Example callback file
```python
def update_member(op: str, **data):
    member_id = data.pop("member")
    # logic here
    return {"status": 200}


def setup(routes):
    routes["update_member"] = update_member()  # add your handlers here
```