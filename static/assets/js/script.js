const btn_menu = document.querySelector(".bi-list")
const menu = document.querySelector(".menu")
const header = document.querySelector(".header")
const content = document.querySelector(".content-body")
const footer = document.querySelector(".footer")

btn_menu.addEventListener("click",()=>{
    menu.classList.toggle("wrapper")
    header.classList.toggle("wrapper")
    content.classList.toggle("wrapper")
    footer.classList.toggle("wrapper")
})

let plus = document.querySelectorAll(".arrow")
        
plus.forEach((plusBtn)=>{
    plusBtn.addEventListener("click",(e)=>{
        let plusParent = e.target.parentElement
        plusParent.classList.toggle("show")
    })
})

// Column Toggle
checkboxes = document.getElementsByName('col');

function toggle(source) {
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
        checkboxes[i].click()
    }
}	

checkboxes.forEach(boton => {
    boton.addEventListener('click', columnaToggle)
    boton.click()
})	

function columnaToggle(e) {
    if (e.target.checked == false) {
        document.querySelectorAll(`.${e.target.id}`).forEach((element)=>{
            element.setAttribute('hidden','')
        })
    }else{
        document.querySelectorAll(`.${e.target.id}`).forEach((element)=>{
            element.removeAttribute('hidden','')
        })
    }
}

if (screen.width < 550) {
    checkboxes.forEach(boton => {
        boton.click()
    })

    document.querySelectorAll(`#name`).forEach((element)=>{
        element.click()
    })
    document.querySelectorAll(`#state`).forEach((element)=>{
        element.click()
    })
}

let checkbox = document.getElementById('show');
let row = document.querySelectorAll('#tablerow');
let estado = document.querySelectorAll('#stateUser');

checkbox.addEventListener("click",mostrar)

const STATE_PARAM = "inactive"

if (checkbox.checked==false) {
    rowBucle("none",STATE_PARAM)
}

function mostrar(){
    if (checkbox.checked==true) {
        rowBucle("",STATE_PARAM)
    }else if (checkbox.checked==false){
        rowBucle("none",STATE_PARAM)
    }
}

function rowBucle(display, state) {
    for (let index = 0; index < estado.length; index++) {
        if (estado[index].textContent.toLowerCase() == `${state}`) {
            for (let index = 0; index < row.length; index++) {
              if (estado[index].textContent.toLowerCase() == `${state}`) {
                row[index].setAttribute('style',`display:${display}`);
              }
            }
        }
    }
}

const switchState = document.querySelectorAll("#flexSwitchCheckDefault")

switchState.forEach((element)=>{
    element.addEventListener("click",(e)=>{
        e.target.parentElement.click()
    })
})
