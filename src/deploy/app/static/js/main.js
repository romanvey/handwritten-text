let submit = (e) => {
    e.preventDefault()
    let text = inputForm.input.value;
    let style = 0;
    route = "http://localhost:8000/get_text"
    body = {text: text, style:style}

    fetch(route, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        mode: 'no-cors',
        body: body
    }).then(response => {
        response.json().then(data => console.log(data));
    })
}

let container = document.createElement('div');
container.className = 'container'

let inputWrapper = document.createElement('div')
inputWrapper.className = 'input-wrapper'

let inputForm = document.createElement('form')
inputForm.className = 'input-form'
inputForm.onsubmit = (e) => {submit(e)};
    
let inputField = document.createElement('input');
inputField.type = 'text';
inputField.className = 'input-field';
inputField.placeholder = 'Write your masterpiece here'
inputField.name = 'input';
    
let inputBtn = document.createElement('button');
inputBtn.type = 'submit';
inputBtn.className = 'input-submit-btn';
inputBtn.innerText = 'Generate!'

let outputWrapper = document.createElement('div');
outputWrapper.className = 'output-wrapper'

inputForm.appendChild(inputField)
inputForm.appendChild(inputBtn)
inputWrapper.appendChild(inputForm)
container.appendChild(inputWrapper)

container.appendChild(outputWrapper)
document.body.appendChild(container)

