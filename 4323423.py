import streamlit as st
import plotly.graph_objects as go
import numpy as np
from sympy import sympify, lambdify, symbols

# 1. Настройка страницы сайта
st.set_page_config(page_title="3D Графики", layout="wide")
st.title("🎛️ Интерактивный 3D График")

st.sidebar.header("Ввод формулы")

# Поле ввода уравнения
user_input = st.sidebar.text_input(
    "Введите уравнение (z = ...):", 
    value="sin(x^2 + y^2) / sqrt(x^2 + y^2)"
)

# Ползунок для дыры в центре
hole_size = st.sidebar.slider("Размер дыры в центре", 0.0, 1.0, 0.1, 0.05)

# 2. Создаем сетку координат
x_arr = np.linspace(-5, 5, 200)
y_arr = np.linspace(-5, 5, 200)
X, Y = np.meshgrid(x_arr, y_arr)
R = np.sqrt(X**2 + Y**2)

# Очистка строки ввода
clean_formula = user_input.replace("z =", "").replace("Z =", "").strip()

try:
    # Заменяем знак степени ^ на питоновский **
    clean_formula = clean_formula.replace("^", "**")
    
    # Символы для математического парсера
    x_sym, y_sym = symbols('x y')
    
    # Переводим текст в математику SymPy
    sympy_expr = sympify(clean_formula)
    
    # Превращаем в функцию NumPy с защитой от ошибок деления на ноль
    compiled_func = lambdify((x_sym, y_sym), sympy_expr, modules=['numpy'])
    
    with np.errstate(divide='ignore', invalid='ignore'):
        Z = compiled_func(X, Y)
    
    if isinstance(Z, (int, float)):
        Z = np.full_like(X, float(Z))
        
    # Принудительно делаем дыру в центре
    if hole_size > 0:
        Z[R < hole_size] = np.nan

    # 3. Строим график (Используем палитру 'icefire', она точно есть в списке)
    fig = go.Figure(data=[go.Surface(
        x=x_arr, 
        y=y_arr, 
        z=Z, 
        colorscale='icefire',  # Гарантированно рабочая палитра сине-красного цвета
        colorbar=dict(thickness=20, len=0.6)
    )])

    # Настройки интерактива
    fig.update_layout(
        title="Зажмите ЛКМ для вращения | Колесико мыши для приближения",
        autosize=True,
        width=950,
        height=750,
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    # Отображаем на сайте
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Не удалось распознать формулу. Ошибка: {e}")

st.sidebar.markdown("""
### 💡 Как писать формулы:
* **Степень:** используйте `^` (например, `x^2 + y^2`).
* **Умножение:** можно слитно (например, `4x`, `xy`, `3cos(x)`).
* **Функции:** `sin(x)`, `cos(y)`, `tan(x)`, `sqrt(x)`, `exp(x)`.
""")
