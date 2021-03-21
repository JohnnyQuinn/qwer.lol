const tooltip_container = document.getElementById('tooltip-container')
const carousel = document.getElementById('abilityVideoCarousel')

const p_video = document.getElementById('p_vid')
const q_video = document.getElementById('q_vid')
const w_video = document.getElementById('w_vid')
const e_video = document.getElementById('e_vid')
const r_video = document.getElementById('r_vid')
const videos = [p_video, q_video, w_video, e_video, r_video]

const p_button = document.getElementById('p_button')
const q_button = document.getElementById('q_button')
const w_button = document.getElementById('w_button')
const e_button = document.getElementById('e_button')
const r_button = document.getElementById('r_button')

const p_tooltip = document.getElementById('p_tooltip')
const q_tooltip = document.getElementById('q_tooltip')
const w_tooltip = document.getElementById('w_tooltip')
const e_tooltip = document.getElementById('e_tooltip')
const r_tooltip = document.getElementById('r_tooltip')

p_button.onclick = function(){
    hideTooltips(0);
    handleAutoplay(0);
//     p_tooltip.hidden = false;
};

q_button.onclick = function(){
    hideTooltips(1);
    handleAutoplay(1);
    // q_tooltip.hidden = false;
};

w_button.onclick = function(){
    hideTooltips(2);
    handleAutoplay(2);
    // w_tooltip.hidden = false;
};

e_button.onclick = function(){
    hideTooltips(3);
    handleAutoplay(3);
    // e_tooltip.hidden = false;
};

r_button.onclick = function(){
    hideTooltips(4);
    handleAutoplay(4);
    // r_tooltip.hidden = false;
};

function hideTooltips(skip){
    for (let i = 0; i < tooltip_container.children.length; i++){
        if(i === skip){
            tooltip_container.children[i].hidden = false;
            continue;
        }
        tooltip_container.children[i].hidden = true;
    }
}

function handleAutoplay(skip) {
    for (let i = 0; i < 5; i++){
        if(i === skip){
            videos[i].play();
            continue;
        }
        videos[i].pause();
        videos[i].currentTime = 0;
    }
}