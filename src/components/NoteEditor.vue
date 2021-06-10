<template>
  <div>
    <div class="editor mt-1">
      <h3 class="mb-3">メモを追加</h3>
      <div class="mb-3">
        <label class="form-label">タイトル</label>
        <input type="text" class="form-control" v-model="note.title" />
      </div>
      <div class="mb-3">
        <label class="form-label">本文</label>
        <textarea
          class="form-control"
          style="height: 30vh"
          v-model="note.body"
        ></textarea>
      </div>
      <div class="mb-4">
        <label class="form-label">タグ</label>
        <input
          type="text"
          class="form-control"
          placeholder="クリックで追加"
          readonly
          :value="joinedTags"
          @click="openTagPicker"
        />
      </div>
      <div class="row">
        <div class="col-auto">
          <button class="btn btn-secondary" @click="cancelEdit">戻る</button>
        </div>
        <div class="col-auto" v-if="note.id == null">
          <button class="btn btn-primary" @click="emitCreate">追加</button>
        </div>
        <div class="col-auto" v-else>
          <button class="btn btn-primary" @click="emitUpdate">更新</button>
        </div>
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
.editor {
  margin: 0 auto;
  max-width: 500px;
}
</style>