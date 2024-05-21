from flask import Flask, request, render_template, redirect, url_for
from tel import TOKEN, main, dispatcher  # تحديث الاستيراد هنا

# إنشاء تطبيق Flask
app = Flask(__name__)

# إعداد البوت داخل تطبيق Flask
main()

# قائمة لتخزين التحديثات
updates_list = ["postooo"]  # إضافة العبارة "postooo" للقائمة عند بدء التشغيل

# عرض صفحة index.html عند الوصول إلى الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html', updates=updates_list)

# تعريف نقطة الوصول لاستقبال الرسائل الواردة من التيليجرام
@app.route('/<token>/', methods=['POST'])
def webhook_handler(token):
    if token == TOKEN:
        update = request.get_json()
        dispatcher.process_update(update)
        
        # إضافة التحديث إلى القائمة
        updates_list.append(update)
        
        # إعادة توجيه المستخدم إلى الصفحة الرئيسية
        return redirect(url_for('index'))
    return 'Invalid token'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=0000, debug=True)
