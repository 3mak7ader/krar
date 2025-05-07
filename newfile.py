import os
import json
from getpass import getpass

# ملفات التخزين
USERS_FILE = "users.json"
DEBTS_FILE = "debts.json"

# تهيئة الملفات إذا لم تكن موجودة
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump({"hader": {"password": "admin11", "is_admin": True}}, f)

if not os.path.exists(DEBTS_FILE):
    with open(DEBTS_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    """تحميل البيانات من الملفات"""
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    with open(DEBTS_FILE, 'r') as f:
        debts = json.load(f)
    
    return users, debts

def save_data(users, debts):
    """حفظ البيانات إلى الملفات"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    
    with open(DEBTS_FILE, 'w') as f:
        json.dump(debts, f)

def register():
    """إنشاء حساب جديد"""
    users, _ = load_data()
    
    print("\n--- إنشاء حساب جديد ---")
    username = input("اسم المستخدم: ")
    
    if username in users:
        print("هذا المستخدم موجود بالفعل!")
        return
    
    password = getpass("كلمة السر: ")
    confirm_password = getpass("تأكيد كلمة السر: ")
    
    if password != confirm_password:
        print("كلمتا السر غير متطابقتين!")
        return
    
    users[username] = {"password": password, "is_admin": False}
    save_data(users, {})
    print("تم إنشاء الحساب بنجاح!")

def login():
    """تسجيل الدخول"""
    users, _ = load_data()
    
    print("\n--- تسجيل الدخول ---")
    username = input("اسم المستخدم: ")
    password = getpass("كلمة السر: ")
    
    if username not in users or users[username]["password"] != password:
        print("اسم المستخدم أو كلمة السر غير صحيحة!")
        return None
    
    print(f"مرحبًا بك {username}!")
    return username, users[username]["is_admin"]

def add_debt(current_user):
    """إضافة دين جديد"""
    _, debts = load_data()
    
    print("\n--- إضافة دين جديد ---")
    person = input("اسم الشخص: ")
    amount = float(input("المبلغ: "))
    description = input("الوصف (اختياري): ")
    
    if person not in debts:
        debts[person] = []
    
    debts[person].append({
        "creditor": current_user,
        "amount": amount,
        "description": description,
        "paid": False
    })
    
    save_data({}, debts)
    print("تم إضافة الدين بنجاح!")

def search_debts():
    """البحث عن ديون شخص"""
    _, debts = load_data()
    
    print("\n--- البحث عن ديون ---")
    person = input("اسم الشخص للبحث: ")
    
    if person not in debts or not debts[person]:
        print("لا توجد ديون مسجلة لهذا الشخص.")
        return
    
    total = 0
    print(f"\nديون {person}:")
    for i, debt in enumerate(debts[person], 1):
        status = "مسدد" if debt["paid"] else "غير مسدد"
        print(f"{i}. الدائن: {debt['creditor']} | المبلغ: {debt['amount']} | الوصف: {debt['description']} | الحالة: {status}")
        if not debt["paid"]:
            total += debt["amount"]
    
    print(f"\nالمبلغ الإجمالي غير المسدد: {total}")

def pay_debt(current_user):
    """تسديد دين"""
    _, debts = load_data()
    
    print("\n--- تسديد دين ---")
    person = input("اسم الشخص: ")
    
    if person not in debts or not debts[person]:
        print("لا توجد ديون مسجلة لهذا الشخص.")
        return
    
    print(f"\nديون {person}:")
    for i, debt in enumerate(debts[person], 1):
        status = "مسدد" if debt["paid"] else "غير مسدد"
        print(f"{i}. الدائن: {debt['creditor']} | المبلغ: {debt['amount']} | الوصف: {debt['description']} | الحالة: {status}")
    
    try:
        choice = int(input("\nاختر رقم الدين لتسديده (0 للإلغاء): "))
        if choice == 0:
            return
        
        selected = debts[person][choice-1]
        
        if selected["paid"]:
            print("هذا الدين مسدد بالفعل!")
            return
            
        if selected["creditor"] != current_user:
            print("يمكنك فقط تسديد الديون التي أضفتها أنت!")
            return
            
        debts[person][choice-1]["paid"] = True
        save_data({}, debts)
        print("تم تسديد الدين بنجاح!")
    except (ValueError, IndexError):
        print("اختيار غير صحيح!")

def view_all_debts():
    """عرض جميع الديون"""
    _, debts = load_data()
    
    print("\n--- جميع الديون ---")
    if not debts:
        print("لا توجد ديون مسجلة.")
        return
    
    for person, person_debts in debts.items():
        total = 0
        print(f"\nديون {person}:")
        for i, debt in enumerate(person_debts, 1):
            status = "مسدد" if debt["paid"] else "غير مسدد"
            print(f"{i}. الدائن: {debt['creditor']} | المبلغ: {debt['amount']} | الوصف: {debt['description']} | الحالة: {status}")
            if not debt["paid"]:
                total += debt["amount"]
        print(f"المبلغ الإجمالي غير المسدد: {total}")

def admin_panel():
    """لوحة تحكم الأدمن"""
    users, debts = load_data()
    
    print("\n--- لوحة تحكم الأدمن ---")
    print("1. عرض جميع المستخدمين")
    print("2. حذف مستخدم")
    print("3. العودة للقائمة الرئيسية")
    
    choice = input("اختر خيارًا: ")
    
    if choice == "1":
        print("\n--- جميع المستخدمين ---")
        for username, data in users.items():
            print(f"اسم المستخدم: {username} | نوع الحساب: {'أدمن' if data['is_admin'] else 'عادي'}")
    
    elif choice == "2":
        username = input("اسم المستخدم للحذف: ")
        if username == "hader":
            print("لا يمكن حذف حساب الأدمن الرئيسي!")
        elif username in users:
            del users[username]
            save_data(users, debts)
            print("تم حذف المستخدم بنجاح!")
        else:
            print("المستخدم غير موجود!")
    
    elif choice == "3":
        return
    
    else:
        print("اختيار غير صحيح!")

def main():
    """القائمة الرئيسية"""
    current_user = None
    is_admin = False
    
    while True:
        if current_user is None:
            print("\n--- نظام إدارة الديون ---")
            print("1. تسجيل الدخول")
            print("2. إنشاء حساب جديد")
            print("3. خروج")
            
            choice = input("اختر خيارًا: ")
            
            if choice == "1":
                result = login()
                if result:
                    current_user, is_admin = result
            elif choice == "2":
                register()
            elif choice == "3":
                print("مع السلامة!")
                break
            else:
                print("اختيار غير صحيح!")
        else:
            print(f"\n--- القائمة الرئيسية (مرحبًا {current_user}) ---")
            print("1. إضافة دين جديد")
            print("2. البحث عن ديون شخص")
            print("3. تسديد دين")
            print("4. عرض جميع الديون")
            if is_admin:
                print("5. لوحة تحكم الأدمن")
            print("6. تسجيل الخروج")
            
            choice = input("اختر خيارًا: ")
            
            if choice == "1":
                add_debt(current_user)
            elif choice == "2":
                search_debts()
            elif choice == "3":
                pay_debt(current_user)
            elif choice == "4":
                view_all_debts()
            elif choice == "5" and is_admin:
                admin_panel()
            elif choice == "6":
                current_user = None
                is_admin = False
                print("تم تسجيل الخروج بنجاح!")
            else:
                print("اختيار غير صحيح!")

if __name__ == "__main__":
    main()