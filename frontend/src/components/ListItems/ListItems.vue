<template>
  <div class="list_items_menu">
    <keep-alive>
      <component :is="currentComponent"/>
    </keep-alive>
  </div>
</template>

<script setup>
import ChatsList from "@/components/ListItems/UsersList.vue"
import RoomsList from "@/components/ListItems/RoomsList.vue"
import Notifications from "@/components/ListItems/NotifyList.vue"
import {useStore} from "vuex"
import {computed, watch, shallowRef} from "vue"

const store = useStore()

const actualItemMenu = computed(() => store.state.actualItemMenu)

const componentsMap = {
  chats: ChatsList,
  rooms: RoomsList,
  notify: Notifications,
}

const currentComponent = shallowRef(componentsMap[actualItemMenu.value])

watch(actualItemMenu, (newVal) => {
  currentComponent.value = componentsMap[newVal] || null
})
</script>