"""Check registered state handlers."""
from app.services.state_machine import HANDLER_REGISTRY

print('✅ Registered handlers:')
for state in sorted(HANDLER_REGISTRY.keys()):
    print(f'  - {state}')

print(f'\nTotal handlers: {len(HANDLER_REGISTRY)}')
