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
        <button class="btn btn-primary" @click="emitUpdate">Update</button>
      </div>

      <!-- タグ選択画面 -->
      <div id="tagPickerEditer">
        <TagPicker
          :tags="note.tags"
          :visible="isOpenTagPicker"
          @close="isOpenTagPicker = false"
        ></TagPicker>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import bootstrap from "bootstrap"
import { Vue, Options } from 'vue-class-component'

import { Note } from '../models';
import TagPicker from './TagPicker.vue'

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
  isOpenTagPicker = false

  get joinedTags(): string {
    return this.note.tags.map(tag => tag.name).join(' ')
  }

  openTagPicker(e: MouseEvent) {
    e.preventDefault();
    (e.target as HTMLElement).blur()
    this.isOpenTagPicker = true
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