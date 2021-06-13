<!-- ノート1枚のカード -->
<template>
  <div>
    <div class="card" style="width: 320px">
      <div class="card-body p-2">
        <div class="main-contents">
          <div>
            <strong>{{ note.title }}</strong>
          </div>
          <div class="mb-1" style="white-space: pre-wrap">
            {{ note.body }}
          </div>
        </div>
        <div class="mb-1">
          <span
            v-for="tag in note.tags"
            :key="tag.id"
            class="badge bg-secondary me-1 fw-normal"
            >{{ tag.name }}</span
          >
        </div>
        <div class="d-flex align-items-center">
          <div class="h6 m-0">{{ date }}</div>

          <div class="dropdown ms-auto">
            <span
              id="menu"
              style="cursor: pointer; vertical-align: middle"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <img src="@/assets/three-dots.svg" />
            </span>
            <!-- ドロップダウンメニュー -->
            <ul class="dropdown-menu" aria-labelledby="menu">
              <li>
                <button class="dropdown-item" @click="emitEdit">Edit</button>
              </li>
              <li>
                <button class="dropdown-item" @click="emitDelete">
                  Delete
                </button>
              </li>
            </ul>
          </div>
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