import asyncio
import aiohttp

class UnivacKVMTacticalPanel:
    def __init__(self, bridge_control_url: str):
        self.bridge_control_url = bridge_control_url
        self.session = None

    async def initialize(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2.0))

    async def shutdown(self):
        if not self.session:
            return
        await self.session.close()

    async def toggle_antigravity_uplink(self, authorize: bool) -> str:
        if not self.session:
            return "KVM_OFFLINE"
        
        payload = {"target_system": "ANTIGRAVITY", "uplink_authorized": authorize}
        
        try:
            async with self.session.post(self.bridge_control_url + "/toggle", json=payload) as response:
                if response.status == 200:
                    return "ANTIGRAVITY_STATE_CHANGED"
                return "NETWORK_REJECT"
        except Exception:
            return "FAULT"

    async def toggle_aviation_uplink(self, authorize: bool) -> str:
        if not self.session:
            return "KVM_OFFLINE"
        
        payload = {"target_system": "AVIATION", "uplink_authorized": authorize}
        
        try:
            async with self.session.post(self.bridge_control_url + "/toggle", json=payload) as response:
                if response.status == 200:
                    return "AVIATION_STATE_CHANGED"
                return "NETWORK_REJECT"
        except Exception:
            return "FAULT"
