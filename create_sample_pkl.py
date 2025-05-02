import pickle

# Sample data
data = {
    "name": "Retro Pickle Viewer",
    "version": "1.0",
    "features": ["Upload Pickle", "View Contents", "Retro Theme"],
    "author": {
        "name": "Smarth",
        "contact": "Smarth@example.com"
    }
}

# Save it as a .pkl file
with open('test.pkl', 'wb') as f:
    pickle.dump(data, f)

print("✅ Sample test.pkl created!")
