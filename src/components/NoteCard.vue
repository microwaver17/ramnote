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
                <a class="dropdown-item" @click="onClickEdit">Edit</a>
              </li>
              <li>
                <a
                  class="dropdown-item"
                  data-bs-toggle="modal"
                  data-bs-target="#deletemodal"
                  >Delete</a
                >
              </li>
            </ul>
          </div>
        </div>
        <div>{{ note.body }}</div>
        <div>
          <span
            v-for="tag_str in note.tags_str"
            :key="tag_str"
            class="border rounded text-white bg-secondary p-1 float-start"
            >{{ tag_str }}</span
          >
        </div>
      </div>
    </div>

    <div id="deletemodal" class="modal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body">
            <p>削除してもよろしいですか？</p>
          </div>
          <div class="modal-footer">
            <button data-bs-dismiss="modal" class="btn btn-primary">
              Cancel
            </button>
            <button
              data-bs-dismiss="modal"
              class="btn btn-danger"
              @click="onClickDelete"
            >
              OK
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";

import { Note } from "../model"
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

  onClickEdit() {
    this.$emit('edit', this.note)
  }
  onClickDelete() {
    this.$emit('delete', this.note)
  }
}
</script>

<style scoped>
</style>