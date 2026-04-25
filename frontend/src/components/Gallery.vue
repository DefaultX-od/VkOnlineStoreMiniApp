<script setup>
import { onMounted, ref } from 'vue';
import GalleryObject from './GalleryObject.vue';


const props = defineProps({
    album:{
        type: Array,
        default: () => []
    }
})

const gallery = ref(null)
const galleryDots = ref(null)

var active = ref(0)
var startX = ref(0)
var endX = ref(0)
var isTouchingGallery = ref(false)

function reloadGallery(){
    let offset = -active.value * 100
    gallery.value.style.transform = `translateX(${offset}%)`

    const dots = galleryDots.value.children

    Array.from(dots).forEach((dot, index)=>{
        dot.classList.toggle('active', index === active.value)
    })
}

function onTouchStart(event){
    if (!gallery.value || !gallery.value.contains(event.target)) return;
    isTouchingGallery.value = true
    startX.value = event.touches[0].clientX
}

function onTouchMove(event){
    if (!isTouchingGallery.value) return;
    event.preventDefault()
    endX.value = event.touches[0].clientX
}
function onTouchEnd(){
    if (!isTouchingGallery.value) return;
    let diff = startX.value - endX.value;

    if (diff > 50 && active.value < props.album.length - 1) {
        active.value += 1;
    } else if (diff < -50 && active.value > 0) {
        active.value -= 1;
    }
    reloadGallery();
    isTouchingGallery.value = false;
}
onMounted(() => {
    reloadGallery();
});
</script>

<template>
    <div v-if="album.length > 0"
        class="gallery-container"
        @touchstart="onTouchStart"
        @touchmove="onTouchMove"
        @touchend="onTouchEnd"
        >
    <div class="gallery" ref="gallery">
        <GalleryObject
        v-for="img in album" 
        :key="img"
        :imgSource="img"
        ref="galleryObjects"
        />
    </div>
    <ul class="gallery-items-dots" ref="galleryDots">
        <li class="active"></li>
        <li v-for="i in album.length-1"></li>
    </ul>
</div>
<div  v-else class="gallery-container">
    <div class="gallery" ref="gallery">
        <GalleryObject />
    </div>
    <ul class="gallery-items-dots" ref="galleryDots">
        <li class="active"></li>
    </ul>
</div>
</template>

<style scoped>
.gallery-container {
    overflow: hidden;
    max-width: 100%;
    min-width: 100%;
}

.gallery {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    transition: transform 0.3s ease;
    width: 100%;
    min-width: 100%;
}
.gallery-items-dots{
    background-color: var(--color-bg-secondary);
    bottom: 10px;
    left: 0;
    width: 100%;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
}

.gallery-items-dots li{
    list-style: none;
    width: 5px;
    height: 5px;
    background-color: var(--color-accent-semi-transparent);
    margin: 5px;
    border-radius: 20px;
}

.gallery-items-dots li.active{
    width: 15px;
    background-color: var(--color-accent);
}
</style>