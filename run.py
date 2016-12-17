"""Dev deployment script.
"""

from watsup import app

app.run(debug=True, port=8080, host='0.0.0.0')
