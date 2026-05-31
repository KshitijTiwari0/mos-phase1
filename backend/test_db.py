# backend/test_db.py
import os
from app.db.database import engine, SessionLocal
from app.db import models

def test_database_initialization():
    print("=" * 60)
    print("📦 STARTING DATABASE SCHEMA INITIALIZATION TEST...")
    print("=" * 60)

    # 1. Purani DB file ko clear karna agar wo exist karti hai taaki fresh initialization ho
    db_filename = "mos_phase1.db"
    if os.path.exists(db_filename):
        print(f"🧹 Found existing {db_filename}, removing for a clean test...")
        try:
            os.remove(db_filename)
        except Exception as e:
            print(f"⚠️ Could not remove file, continuing anyway: {e}")

    # 2. Tables Create karna
    print("\n[Step 1] Creating all tables using SQLAlchemy Metadata...")
    try:
        models.Base.metadata.create_all(bind=engine)
        print("✅ Success: Tables successfully mapped and created in SQLite!")
    except Exception as e:
        print(f"❌ Error: Database table generation failed: {e}")
        return

    # 3. Session open karke test record insert karna (Validation check)
    print("\n[Step 2] Testing Database Write/Read Operations...")
    db = SessionLocal()
    try:
        # Create a mock tenant record
        test_tenant = models.Tenant(id="tenant_test_123", name="Test Business Corp")
        db.add(test_tenant)
        db.commit()
        print("✅ Success: Inserted test record into 'tenants' table!")

        # Query the record back
        fetched_tenant = db.query(models.Tenant).filter(models.Tenant.id == "tenant_test_123").first()
        if fetched_tenant and fetched_tenant.name == "Test Business Corp":
            print(f"✅ Success: Verified fetched data safely from DB! (Tenant Name: {fetched_tenant.name})")
        else:
            print("❌ Error: Verification failed. Data mismatch or record missing.")
            
    except Exception as e:
        print(f"❌ Error: Session transaction operation failed: {e}")
    finally:
        db.close()
        print("\n" + "=" * 60)
        print("🎉 DB SMOKE TEST COMPLETED!")
        print("=" * 60)

if __name__ == "__main__":
    test_database_initialization()