

class Agent:
    def __init__(self, agent_id):
        self.id = agent_id
        self.hpid = None
        self.name = None
        self.address_street = None
        self.address_zip_code = None
        self.address_city = None
        self.address_country = None
        self.email_address_general = None
        self.phone_no_general = None

    def __str__(self):
        return self.name

    def get_agent_info(self):
        pass
