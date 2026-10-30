import sys

class GiryInterpreter:
    def __init__(self):
        self.variables = {}  # Собственная память языка Giry

    def evaluate_expr(self, expr_str):
        expr_str = expr_str.strip()
        
        # Если это число
        try:
            if '.' in expr_str:
                return float(expr_str)
            return int(expr_str)
        except ValueError:
            pass

        # Если это строка в кавычках ("текст")
        if expr_str.startswith('"') and expr_str.endswith('"'):
            return expr_str[1:-1]
        if expr_str.startswith("'") and expr_str.endswith("'"):
            return expr_str[1:-1]

        # Если это имя переменной
        if expr_str in self.variables:
            return self.variables[expr_str]

        # Простейшая математика (например, a + b)
        for op in ['+', '-', '*', '/']:
            if op in expr_str:
                parts = expr_str.split(op)
                if len(parts) == 2:
                    left = self.evaluate_expr(parts[0])
                    right = self.evaluate_expr(parts[1])
                    if op == '+': return left + right
                    if op == '-': return left - right
                    if op == '*': return left * right
                    if op == '/': return left / right if right != 0 else 0

        raise SyntaxError(f"Неизвестное выражение или переменная: '{expr_str}'")

    def run_line(self, line, line_num):
        line = line.strip()
        # Пропускаем пустые строки и комментарии
        if not line or line.startswith('#'):
            return

        # Убираем точку с запятой в конце, если есть
        if line.endswith(';'):
            line = line[:-1].strip()

        # Команда вывода: push.text(...)
        if line.startswith('push.text(') and line.endswith(')'):
            content = line[10:-1]
            val = self.evaluate_expr(content)
            print(val)
            return

        # Объявление переменной: let имя = значение
        if line.startswith('let '):
            parts = line[4:].split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                var_val = self.evaluate_expr(parts[1].strip())
                self.variables[var_name] = var_val
                return

        # Переприсваивание: имя = значение
        if '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                var_name = parts[0].strip()
                var_val = self.evaluate_expr(parts[1].strip())
                if var_name in self.variables:
                    self.variables[var_name] = var_val
                    return
                else:
                    raise NameError(f"Переменная '{var_name}' не объявлена!")

        raise SyntaxError(f"Синтаксическая ошибка в строке {line_num}: '{line}'")

    def execute(self, source_code):
        print("--- КОМПИЛЯТОР GIRY ЗАПУЩЕН (ЧЕСТНЫЙ ПАРСИНГ) ---")
        lines = source_code.split('\n')
        for i, line in enumerate(lines, 1):
            try:
                self.run_line(line, i)
            except Exception as e:
                print(f"[GIRY FATAL ERROR] Строка {i}: {e}")
                break

# --- ТЕСТИРУЕМ НАШ ЯЗЫК ---
if __name__ == '__main__':
    script = """
    # Приветствие от iovozaurs-team
    push.text("Привет! Это Giry — самый медленный язык на свете.")
    
    let a = 300;
    let b = 150;
    let result = a + b * 2;
    
    push.text("Результат вычислений переменной result:");
    push.text(result);
    
    # Проверка переприсваивания
    result = result + 50;
    push.text("После обновления:");
    push.text(result);
    """

    engine = GiryInterpreter()
    engine.execute(script)