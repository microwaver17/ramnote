<!-- ノート1枚のカード -->
<template>
  <div>
    <div class="card">
      <div class="card-body">
        <div class="clearfix">
          <div class="float-start">
            <h5 class="card-title">{{ note.title }}</h5>
            <h6 class="card-subtitle">{{ date }}</h6>
          </div>
          <div class="dropdown">
            <a
              id="menu"
              class="btn float-end"
              data-bs-toggle="dropdown"
              aria-expanded="false"
              ><img class="float-end" src="@/assets/three-dots.svg"
            /></a>
            <!-- ドロップダウンメニュー -->
            <ul class="dropdown-menu" aria-labelledby="menu">
              <li>
                <a class="dropdown-item" @click="emitEdit">Edit</a>
              </li>
              <li>
                <a class="dropdown-item" @click="emitDelete">Delete</a>
              </li>
            </ul>
          </div>
        </div>
        <div>{{ note.body }}</div>
        <div>
          <span
            v-for="tag in note.tags"
            :key="tag.id"
            class="border rounded text-white bg-secondary p-1 float-start"
            >{{ tag.name }}</span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";

import { Note } from "../models"
import NoteEditor from "./NoteEditor.vue"

@Options({
  emits: ['edit', 'delete'],
  components: {
    NoteEditor,
  },
  props: {
    note: Note
  },
})
export default class NoteCard extends Vue {
  note!: Note

  get date(): string {
    let s = '' +
      this.note.date.getFullYear() +
      '/' +
      (this.note.date.getMonth() + 1) +
      '/' +
      this.note.date.getDate()

    return s
  }

  emitEdit() {
    this.$emit('edit', this.note)
  }
  emitDelete() {
    this.$emit('delete', this.note)
  }
}
</script>

<style scoped>
</style>