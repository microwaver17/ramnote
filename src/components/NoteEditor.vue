<template>
  <div>
    <div
      class="modal"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
    >
      <div
        class="
          modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg
        "
      >
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-body">
              <div>
                <label>Title</label>
                <input type="text" class="form-control" v-model="note.title" />
                <label>Body</label>
                <textarea
                  class="form-control"
                  style="height: 30vh"
                  v-model="note.body"
                ></textarea>
                <label>Tags</label>
                <input
                  :id="'formTags' + id()"
                  type="text"
                  class="form-control"
                  :value="joinedTags()"
                />
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">
              Cancel
            </button>
            <div v-if="!note.id">
              <button class="btn btn-primary">Create</button>
            </div>
            <div v-else>
              <button class="btn btn-primary">Update</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- タグ選択画面 -->
    <div :id="'tagPicker' + id()">
      <TagPicker v-model="note.tags"></TagPicker>
    </div>
  </div>
</template>

<script lang="ts">
import { Note } from '../model';
import { Vue, Options } from 'vue-class-component'
import TagPicker from './TagPicker.vue'
import bootstrap from "bootstrap"

@Options({
  components: {
    TagPicker,
  },
  props: {
    note: Note
  }
})
export default class NoteEditor extends Vue {
  note!: Note

  id(): string {
    return this.note.id ?? 'null'
  }

  mounted(): void {
    // タグ入力フォームをクリックすると、タグ選択画面を開く
    const formTags = document.getElementById('formTags' + this.id())
    if (formTags) {
      formTags.addEventListener('click', (e) => {
        e.preventDefault()
        formTags.blur()

        // ダイアログを開く
        const tagPicker = document.querySelector(
          '#tagPicker' + this.id() + ' .modal')
        if (tagPicker) {
          console.log(tagPicker)
          let modal = new bootstrap.Modal(tagPicker)
          modal.show()
        }
      })
    }
  }

  joinedTags(): string {
    if (!this.note.id) {
      return ''
    }
    return this.note.tags_str.join(' ')
  }
}
</script>

<style scoped>
</style>