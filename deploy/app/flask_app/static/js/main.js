let submit = (e) => {
    e.preventDefault()
    alert(inputForm.input.value);
    
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

