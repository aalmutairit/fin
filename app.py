from flask import Flask, render_template, request

app = Flask(__name__)

# تحديد معامل التكلفة بناءً على عدد المركبات
def get_cost_factor(vehicle_count, category):
    if category == "non_hazardous":
        if vehicle_count < 10:
            return 0.8, 1000  # معامل التكلفة منخفض
        elif 10 <= vehicle_count <= 50:
            return 1.0, 3000  # معامل التكلفة متوسط
        else:
            return 1.3, 5000  # معامل التكلفة مرتفع
    elif category == "hazardous":
        if vehicle_count < 5:
            return 0.8, 1000  # معامل التكلفة منخفض
        elif 5 <= vehicle_count <= 30:
            return 1.0, 3000  # معامل التكلفة متوسط
        else:
            return 1.3, 5000  # معامل التكلفة مرتفع

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        main_activity = request.form.get("main_activity")
        sub_activities = request.form.getlist("sub_activity")  # استخدام getlist لاختيار أكثر من نشاط فرعي
        vehicle_counts = request.form.getlist("vehicle_count")  # قائمة عدد المركبات
        cost_factors = []

        # تحديد خط الأساس بناءً على النشاط الرئيسي
        base_cost = 7500 if main_activity == "non_hazardous" else 10000
        total_cost = 0
        max_review_cost = 0

        # معالجة الأنشطة الفرعية مع عدد المركبات الخاص بكل نشاط
        for sub_activity, vehicle_count in zip(sub_activities, vehicle_counts):
            if vehicle_count.strip():  # التأكد من إدخال عدد مركبات
                vehicle_count = int(vehicle_count)
                cost_factor, review_cost = get_cost_factor(vehicle_count, main_activity)
                # حساب التكلفة لكل نشاط فرعي
                total_cost += base_cost * cost_factor  # ضرب خط الأساس في معامل التكلفة
                max_review_cost = max(max_review_cost, review_cost)

        # إضافة المقابل المالي لتدقيق الطلب
        total_cost += max_review_cost + 500  # إضافة تكلفة تقديم الطلب الثابتة
        result = f"The total cost is {total_cost} SAR"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
