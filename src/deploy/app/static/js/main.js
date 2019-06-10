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
        response.json().then(data => renderImage(data.img_link));
    })
}

let renderImage = (img_link) => {
    let img = document.createElement('img')
    img.className = "output-img"
    img.src = img_link
    outputImgWrapper.innerHTML = null;
    outputImgWrapper.appendChild(img)
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

let inputRadioContainer = document.createElement('div');
inputRadioContainer.className = 'input-radio-container';

["casual", "italic", "bold"].forEach((name) => {
    let btn = document.createElement('input')
    btn.type = 'radio'
    btn.id = name
    btn.className = 'input-radio-btn'
    btn.name = "text-style"
    btn.value = name
    inputRadioContainer.appendChild(btn)

    let btnLabel = document.createElement('label')
    btnLabel.className = 'input-radio-label'
    btnLabel.innerText = name
    btnLabel.htmlFor = name
    inputRadioContainer.appendChild(btnLabel)
})
inputRadioContainer.firstChild.checked = true


let outputWrapper = document.createElement('div');
outputWrapper.className = 'output-wrapper'

let outputImgWrapper = document.createElement('div');
outputImgWrapper.className = 'output-img-wrapper'

outputWrapper.appendChild(outputImgWrapper)
inputForm.appendChild(inputField)
inputForm.appendChild(inputRadioContainer)
inputForm.appendChild(inputBtn)
inputWrapper.appendChild(inputForm)
container.appendChild(inputWrapper)

container.appendChild(outputWrapper)
document.body.appendChild(container)

