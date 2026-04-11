"""
MZB_ Application Runner
"""

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database created with MZB_ prefix")
        print("🎯 MzansiBuilds running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)