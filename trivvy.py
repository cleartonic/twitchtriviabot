from src.bot import Trivvy
from src.scanner import scanloop

app = Trivvy(scanloop)
app.run()
