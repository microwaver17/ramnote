<template>
  <div>
    <div v-if="note">
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
        @click="openTagPicker"
      />

      <button class="btn btn-secondary" @click="cancelEdit">Cancel</button>
      <div v-if="note.id == null">
        <button class="btn btn-primary" @click="emitCreate">Create</button>
      </div>
      <div v-else>
        <button class="btn btn-primary" @clic="emitUpdate">Update</button>
      </div>

      <!-- タグ選択画面 -->
      <div id="tagPickerEditer">
        <TagPicker v-model:tags="note.tags"></TagPicker>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import bootstrap from "bootstrap"
import { Vue, Options } from 'vue-class-component'

import { Note } from '../models';
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

  openTagPicker(e: MouseEvent) {
    e.preventDefault();
    (e.target as HTMLElement).blur()

    // ダイアログを開く
    const tagPicker = document.querySelector('#tagPickerEditer .modal')
    if (!tagPicker) {
      return
    }
    let modal = new bootstrap.Modal(tagPicker)
    modal.show()
  }

  get joinedTags(): string {
    if (this.note.id == null) {
      return ''
    }
    return this.note.tags.map(tag => tag.name).join(' ')
  }

  cancelEdit() {
    this.$emit('cancel')
  }

  emitCreate() {
    this.$emit('create')
  }

  emitUpdate() {
    this.$emit('update')
  }

}
</script>

<style scoped>
</style>