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
            class="badge bg-success me-1 fw-normal"
            >{{ tag.name }}</span
          >
        </div>
        <div class="d-flex align-items-center">
          <div class="h6 m-0">{{ date }}</div>

          <div class="ms-auto">
            <span
              class="me-2"
              style="cursor: pointer; vertical-align: middle"
              @click="emitDelete"
            >
              <img src="@/assets/x.svg" style="width: 1.2em; height: 1.2em" />
            </span>
            <span
              style="cursor: pointer; vertical-align: middle"
              @click="emitEdit"
            >
              <img src="@/assets/pencil-fill.svg" />
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";

import { Note } from "../models";
import NoteEditor from "./NoteEditor.vue";

@Options({
  emits: ["edit", "delete"],
  components: {
    NoteEditor,
  },
  props: {
    note: Note,
  },
})
export default class NoteCard extends Vue {
  note!: Note;

  get date(): string {
    let s =
      "" +
      this.note.date.getFullYear() +
      "/" +
      (this.note.date.getMonth() + 1) +
      "/" +
      this.note.date.getDate();

    return s;
  }

  emitEdit(): void {
    this.$emit("edit", this.note);
  }
  emitDelete(): void {
    this.$emit("delete", this.note);
  }
}
</script>

<style scoped></style>
