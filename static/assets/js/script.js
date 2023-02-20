// Loader
window.addEventListener("load",()=>{
    const loader = document.querySelector(".loader-content")
    loader.style.opacity = 0
    loader.style.visibility = "hidden"
})

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

    if (menu.classList.contains("wrapper")) {
        localStorage.setItem("sidebar", "off")
    }else{
        localStorage.setItem("sidebar", "on")
    }
})

if (localStorage.getItem("sidebar") == "off") {
    btn_menu.click()
}

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
    boton.checked=true
})	

function columnaToggle(e) {
    if (e.target.checked == false) {
        document.querySelectorAll(`.${e.target.id}`).forEach((element)=>{
            element.setAttribute('hidden','')
        })
        localStorage.setItem(`${e.target.id}`, "false")
    }else{
        document.querySelectorAll(`.${e.target.id}`).forEach((element)=>{
            element.removeAttribute('hidden','')
        })
        localStorage.setItem(`${e.target.id}`, "true")
    }
}

checkboxes.forEach((element)=>{
    if (localStorage.getItem(element.id) == null) {
        localStorage.setItem(element.id, "true")
    }

    if (localStorage.getItem(element.id) == "true") {
        document.querySelectorAll(`.${element.id}`).forEach((element)=>{
            element.removeAttribute('hidden','')
        })
        document.getElementById(`${element.id}`).checked=true
    }else{
        document.querySelectorAll(`.${element.id}`).forEach((element)=>{
            element.setAttribute('hidden','')
        })
        document.getElementById(`${element.id}`).checked=false
    }
})

// if (screen.width < 550) {
//     checkboxes.forEach(boton => {
//         boton.click()
//     })

//     document.querySelectorAll(`#name`).forEach((element)=>{
//         element.click()
//     })
//     document.querySelectorAll(`#state`).forEach((element)=>{
//         element.click()
//     })
// }

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
        localStorage.setItem("showHidden", true)
    }else if (checkbox.checked==false){
        rowBucle("none",STATE_PARAM)
        localStorage.setItem("showHidden", false)
    }
}

if (localStorage.getItem("showHidden") == "true") {
   checkbox.click()
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
