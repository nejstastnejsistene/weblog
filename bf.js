var code = $('#bf').text();
var codePtr = 0;
var tape = [];
var ptr = 0;
var stack = [];

var get = function () { return tape[ptr] || 0; }

while (codePtr < code.length) {
  var ch = code[codePtr++];
  switch (ch) {
    case '>': ptr++; break;
    case '<': ptr--; break;
    case '+': tape[ptr] = get() + 1; break;
    case '-': tape[ptr] = get() - 1; break;
    case ',': console.log('Input not implemented.'); break;
    case '.': document.write(String.fromCharCode(get())); break;
    case '[': if (get() != 0) stack.push(codePtr);
              else {
                var depth = 1;
                while (!(ch == ']' && depth == 0)) {
                  ch = code[codePtr++];
                  if      (ch == '[') depth++;
                  else if (ch == ']') depth--;
                }
             } break;
    case ']': codePtr = stack.pop() - 1; break;
  }
}
