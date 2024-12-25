from flask import Flask, render_template, request

app = Flask(__name__)

# تحديد معامل التكلفة بناءً على نوع النشاط (الجمع والنقل أو المعالجة)
def get_cost_factor(process_capacity, vehicle_count, category):
    if category == "non_hazardous":  # جمع ونقل غير خطر
        if vehicle_count < 10:
            return 0.8, 1000  # معامل التكلفة منخفض
        elif 10 <= vehicle_count <= 50:
            return 1.0, 3000  # معامل التكلفة متوسط
        else:
            return 1.3, 5000  # معامل التكلفة مرتفع
    elif category == "hazardous":  # جمع ونقل خطر
        if vehicle_count < 5:
            return 0.8, 1000  # معامل التكلفة منخفض
        elif 5 <= vehicle_count <= 30:
            return 1.0, 3000  # معامل التكلفة متوسط
        else:
            return 1.3, 5000  # معامل التكلفة مرتفع
    elif category == "waste_processing":  # المعالجة
        if process_capacity < 1:
            return 0.9, 1500  # معامل التكلفة منخفض
        elif 1 <= process_capacity <= 10:
            return 1.1, 3500  # معامل التكلفة متوسط
        else:
            return 1.3, 5000  # معامل التكلفة مرتفع

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        main_activity = request.form.get("main_activity")
        sub_activities = request.form.getlist("sub_activity")  # استخدام getlist لاختيار أكثر من نشاط فرعي
        process_capacities = request.form.getlist("process_capacity")  # قائمة السعة القصوى للمعالجة
        vehicle_counts = request.form.getlist("vehicle_count")  # قائمة عدد المركبات
        cost_factors = []

        # تحديد خط الأساس بناءً على النشاط الرئيسي
        if main_activity == "non_hazardous" or main_activity == "hazardous":  # الجمع والنقل
            base_cost = 7500 if main_activity == "non_hazardous" else 10000
        elif main_activity == "waste_processing":  # المعالجة
            base_cost = 30000
        elif main_activity == "asbestos_removal":  # تفكيك وتغليف الأسبستوس
            base_cost = 10000
        total_cost = 0
        max_review_cost = 0

        # معالجة الأنشطة الفرعية مع السعة القصوى للمعالجة أو عدد المركبات
        for sub_activity, vehicle_count, process_capacity in zip(sub_activities, vehicle_counts, process_capacities):
            if main_activity == "waste_processing" and process_capacity.strip():  # تأكد من إدخال السعة القصوى للمعالجة
                process_capacity = float(process_capacity)
                cost_factor, review_cost = get_cost_factor(process_capacity, vehicle_count, main_activity)
                # حساب التكلفة لكل نشاط فرعي
                total_cost += base_cost * cost_factor  # ضرب خط الأساس في معامل التكلفة
                max_review_cost = max(max_review_cost, review_cost)
            elif main_activity == "asbestos_removal":  # تأكد من تفكيك الأسبستوس
                cost_factor, review_cost = get_cost_factor(process_capacity, vehicle_count, main_activity)
                # حساب التكلفة لكل نشاط فرعي
                total_cost += base_cost * cost_factor  # ضرب خط الأساس في معامل التكلفة
                max_review_cost = max(max_review_cost, review_cost)
            elif (main_activity == "non_hazardous" or main_activity == "hazardous") and vehicle_count.strip():  # تأكد من إدخال عدد المركبات
                vehicle_count = int(vehicle_count)
                cost_factor, review_cost = get_cost_factor(process_capacity, vehicle_count, main_activity)
                # حساب التكلفة لكل نشاط فرعي
                total_cost += base_cost * cost_factor  # ضرب خط الأساس في معامل التكلفة
                max_review_cost = max(max_review_cost, review_cost)

        # إضافة المقابل المالي لتدقيق الطلب
        total_cost += max_review_cost + 500  # إضافة تكلفة تقديم الطلب الثابتة
        result = f"The total cost is {total_cost} SAR"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
