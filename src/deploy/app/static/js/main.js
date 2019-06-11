window.onload = () => {
    initPage();
};

const submit = (e) => {
    displayLoadingAnimation();
    e.preventDefault();
    let text = e.target.input.value;
    let style = e.target.querySelector('input[type=radio]:checked').value;
    let request = {text: text, style: style};

    fetch('/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request)
    }).then(response => {
        if (response.ok) response.json().then(data => displaySvg(data['img']));
        else console.log('Server unavaliable :(')
    })
};

const displayLoadingAnimation = () => {
    let loadingAnimation = document.createElement('div');
    loadingAnimation.className = 'lds-dual-ring';

    let outputImgWrapper = document.getElementById('outputField');
    outputImgWrapper.innerHTML = '';
    outputImgWrapper.appendChild(loadingAnimation); 
};

const displaySvg = svg => {
    let img = document.createElement('div');
    img.className = 'output-img';
    img.innerHTML = svg;

    let outputImgWrapper = document.getElementById('outputField');
    outputImgWrapper.innerHTML = '';
    outputImgWrapper.appendChild(img);
};

const initPage = () => {
    let container = document.createElement('div');
    container.className = 'container';
    container.appendChild(createInput());
    container.appendChild(createOutput());
    document.body.appendChild(container);
};

const createInput = () => {
    let inputWrapper = document.createElement('div');
    inputWrapper.className = 'input-wrapper';
    inputWrapper.appendChild(createForm());
    return inputWrapper;
};

const createOutput = () => {
    let outputWrapper = document.createElement('div');
    outputWrapper.className = 'output-wrapper';
    let outputImgWrapper = document.createElement('div');
    outputImgWrapper.className = 'output-img-wrapper';
    outputImgWrapper.id = 'outputField';
    outputWrapper.appendChild(outputImgWrapper);
    return outputWrapper;
};

const createForm = () => {
    const createInputField = () => {
        let inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.className = 'input-field';
        inputField.placeholder = 'Write your masterpiece here';
        inputField.name = 'input';
        return inputField;
    };
    const createButton = () => {
        let inputBtn = document.createElement('button');
        inputBtn.type = 'submit';
        inputBtn.className = 'input-submit-btn';
        inputBtn.innerText = 'Generate!';
        return inputBtn;
    };
    const createRadioButton = (name, value) => {
        let btn = document.createElement('input');
        btn.type = 'radio';
        btn.className = 'input-radio-btn';
        btn.name = 'text-style';
        btn.value = value;
        btn.id = name;
        return btn;
    };
    const createRadioButtonLabel = (name) => {
        let btnLabel = document.createElement('label');
        btnLabel.className = 'input-radio-label';
        btnLabel.innerText = name;
        btnLabel.htmlFor = name;
        return btnLabel;
    };
    const createRadioButtons = (names) => {
        let inputRadioContainer = document.createElement('div');
        inputRadioContainer.className = 'input-radio-container';
        names.forEach((name, idx) => {
            let btn = createRadioButton(name, idx);
            inputRadioContainer.appendChild(btn);
            let btnLabel = createRadioButtonLabel(name);
            inputRadioContainer.appendChild(btnLabel);
        });
        inputRadioContainer.firstChild.checked = true;
        return inputRadioContainer;
    };

    let inputForm = document.createElement('form');
    inputForm.setAttribute('autocomplete', 'off'); 
    inputForm.className = 'input-form';
    inputForm.onsubmit = (e) => submit(e);
    inputForm.appendChild(createInputField());
    inputForm.appendChild(createRadioButtons(['Child', 'Casual', 'Doctor']));
    inputForm.appendChild(createButton());
    return inputForm;
};
