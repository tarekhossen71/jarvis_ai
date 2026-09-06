
from core.offline_brain import OfflineBrain


brain = OfflineBrain()

response = brain.ask(
    "Hello. Introduce yourself in one short sentence."
)

print("🤖 Offline AI:", response)
