<template>
  <div>
    <div
      class="modal"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      style="z-index: 2000"
      :data-uid="uid"
    >
      <div
        class="
          modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg
        "
      >
        <div class="modal-content" v-if="note">
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
                  :name="'formTags'"
                  type="text"
                  class="form-control"
                  :value="joinedTags"
                  @click="onClickTagForm"
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
    <!-- エディタ用タグ選択画面 -->
    <!--
    <div id="tagPickerEditer">
      <TagPicker v-model:tags="query_tags"></TagPicker>
    </div>
    -->
  </div>
</template>

<script lang="ts">
import bootstrap from "bootstrap"
import { Vue, Options } from 'vue-class-component'

import { Note } from '../model';
import TagPicker from './TagPicker.vue'
import { util } from '../util'

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
  uid = util.uid()

  onClickTagForm(e: MouseEvent) {
    e.preventDefault();
    (e.target as HTMLElement).blur()

    // 自分を閉じる
    const self = document.querySelector(`.modal[data-uid="${this.uid}"]`)
    if (!self) {
      return
    }
    console.log('-----')
    const selfModal = new bootstrap.Modal(self)
    selfModal.hide()

    // ダイアログを開く
    const tagPicker = document.querySelector('#tagPickerEditer .modal')
    if (!tagPicker) {
      return
    }
    let modal = new bootstrap.Modal(tagPicker)
    modal.show()

  }

  get joinedTags(): string {
    if (!this.note.id) {
      return ''
    }
    return this.note.tags_str.join(' ')
  }
}
</script>

<style scoped>
</style>