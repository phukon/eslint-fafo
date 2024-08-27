from rapidfuzz import fuzz

def score_line(str1: str, str2: str) -> float:
    if str1 == str2:
        return 100

    if str1.lstrip() == str2.lstrip():
        whitespace_ratio = abs(len(str1) - len(str2)) / (len(str1) + len(str2))
        score = 90 - whitespace_ratio * 10
        return max(score, 0)

    if str1.strip() == str2.strip():
        whitespace_ratio = abs(len(str1) - len(str2)) / (len(str1) + len(str2))
        score = 80 - whitespace_ratio * 10
        return max(score, 0)

    levenshtein_ratio = fuzz.ratio(str1, str2)
    score = 85 * (levenshtein_ratio / 100)
    return max(score, 0)

def match_code_snippets(snippet1: str, snippet2: str, threshold: float = 80) -> bool:
    score = score_line(snippet1, snippet2)
    return score >= threshold

def code_to_one_liner(code):
    # Remove leading and trailing whitespace from each line
    lines = [line.strip() for line in code.splitlines()]
    # Join the lines together with a single space
    one_liner = ' '.join(lines)
    # Remove any leading or trailing whitespace from the final string
    return one_liner.strip()

multiline_code = """
    <button onClick={addTodo}>Add</button>
    <ul>
        {todos.map(todo => (
            <li
                key={todo.id}
                style={{ textDecoration: todo.completed ? 'line-through' : 'none' }}
                onClick={() => toggleTodo(todo.id)}
            >
                {todo.text}
            </li>
        ))}
    </ul>
"""

# Example usage
snippet1 = """
<button onClick={addTodo}>Add</button> <ul> {todos.map(todo => ( <li key={todo.id} style={{ textDecoration: todo.completed ? 'line-through' : 'none' }} onClick={() => toggleTodo(todo.id)} > {todo.text} </li> ))} </ul>
"""
snippet2 = """
<button onClick={addTodo}>Add</button><ul>{todos.map(todo => <li key={todo.id} style={{ textDecoration: todo.completed ? 'line-through' : 'none' }} onClick={() => toggleTodo(todo.id)}>{todo.text}</li>)}</ul>
"""
is_match = match_code_snippets(snippet1, snippet2, 70)
print(f"Do the snippets match? {'Yes' if is_match else 'No'}")