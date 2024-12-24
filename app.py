from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    activities = {
        "التخزين المؤقت للمواد القابلة للتدوير": None,
        "تجارة المواد القابلة للتدوير": None,
        "تفكيك وتغليف نفايات الاسبستوس": None,
        "التخلص النهائي من النفايات الخطرة": None,
        "التخلص النهائي من النفايات البلدية الصلبة": None,
        "جمع ونقل النفايات غير الخطرة": [
            "جمع ونقل النفايات السكنية",
            "جمع ونقل النفايات التجارية والإدارية",
            "جمع ونقل النفايات الوسائط البحرية",
            "جمع ونقل النفايات الخضراء",
            "جمع ونقل النفايات القابلة لإعادة الاستخدام والتدوير",
            "جمع ونقل نفايات الهدم والبناء",
            "جمع ونقل النفايات الخاملة"
        ],
        "جمع ونقل النفايات الخطرة": [
            "جمع ونقل النفايات الكيميائية",
            "جمع ونقل النفايات الطبية",
            "جمع ونقل الحمأة",
            "جمع ونقل نفايات الزيوت",
            "جمع ونقل نفايات الاسبستوس",
            "جمع ونقل النفايات الالكترونية",
            "جمع ونقل نفايات البطاريات",
            "جمع ونقل الرماد الكربوني",
            "جمع ونقل نفايات الوسائط البحرية"
        ]
    }

    if request.method == 'POST':
        selected_activity = request.form.get('activity')
        selected_sub_activities = request.form.getlist('sub_activities')
        cost_factor = request.form.get('cost_factor')

        if selected_activity:
            base_cost = 0
            if selected_activity == "التخزين المؤقت للمواد القابلة للتدوير":
                base_cost = 10000
            elif selected_activity == "تجارة المواد القابلة للتدوير":
                base_cost = 7500
            elif selected_activity == "تفكيك وتغليف نفايات الاسبستوس":
                base_cost = 15000
            elif selected_activity == "التخلص النهائي من النفايات الخطرة":
                base_cost = 30000
            elif selected_activity == "التخلص النهائي من النفايات البلدية الصلبة":
                base_cost = 20000
            elif selected_activity == "جمع ونقل النفايات غير الخطرة":
                base_cost = 5000
            elif selected_activity == "جمع ونقل النفايات الخطرة":
                base_cost = 10000

            # حساب معامل التكلفة بناءً على الاختيارات
            if cost_factor == "منخفض":
                factor = 0.8
            elif cost_factor == "متوسط":
                factor = 1
            else:
                factor = 1.3

            total_cost = (base_cost * factor) + 1000  # مقبول التكلفة لتدقيق الطلب (افتراض أن المقابل المالي لتدقيق الطلب ثابت)

            return render_template('index.html', activities=activities, total_cost=total_cost, logo_url="static/logo.png")

    return render_template('index.html', activities=activities, logo_url="static/logo.png")


if __name__ == '__main__':
    app.run(debug=True)
