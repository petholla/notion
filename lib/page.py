from dataclasses import dataclass, field

@dataclass
class Page:
    notion: "Notion"
    id: str
    data: dict = field(repr=False)
    
    @property
    def title(self):
        return self.data.get("properties", {}).get("Name", {}).get("title", [{}])[0].get("plain_text", "")