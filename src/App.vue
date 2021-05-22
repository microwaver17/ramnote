<template>
  <div>
    <!-- サイドバー・検索 -->
    <div class="row">
      <div id="sidebar" class="col-3 col-xl-3 col-xxl-2">
        <h2>RAMNOTE</h2>

        <input class="form-control" type="text" />
        <button class="form-control">Search</button>

        <label class="form-label">Tags</label>
        <input
          id="formTags"
          class="form-control"
          type="text"
          :value="query_tags_str"
          @click="onClickTagForm"
        />

        <label class="form-label">From</label>
        <input class="form-control" type="date" />

        <label class="form-label">To</label>
        <input class="form-control" type="date" />

        <button class="form-control" @click="onClickAdd">Add</button>
      </div>

      <!-- ノート一覧 -->
      <div id="contents" class="col-9 col-xl-9 col-xxl-10 ms-auto">
        <div class="row justify-content-center">
          <NoteCard
            class="col-5 col-xl-4 col-xxl-2 m-2"
            v-for="note in notes"
            :key="note.id"
            :note="note"
            @edit="onEditNote"
          ></NoteCard>
        </div>
      </div>
    </div>

    <div>
      <!-- 検索用タグ選択画面 -->
      <div id="tagPickerQuery">
        <TagPicker v-model:tags="query_tags"></TagPicker>
      </div>

      <!-- ノート新規作成エディタ -->
      <div id="editorCreate">
        <NoteEditor :note="newNote"></NoteEditor>
      </div>
      <!-- ノート更新エディタ -->
      <div id="editorUpdate">
        <NoteEditor :note="editNote"></NoteEditor>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import bootstrap from "bootstrap"

import NoteCard from "./components/NoteCard.vue"
import TagPicker from "./components/TagPicker.vue"
import NoteEditor from "./components/NoteEditor.vue"
import { Note, Tag } from "./model"
import { dao } from "./dao"
import { dummyNotes } from "./consts"

@Options({
  components: {
    NoteCard,
    TagPicker,
    NoteEditor,
  },
})
export default class App extends Vue {
  notes: Note[] = []  // 表示するノート
  newNote: Note | null = null
  editNote: Note | null = null
  query_tags: Tag[] = []

  beforeCreate() {
    this.query_tags = []
  }

  // タグをスペースで結合した形式に変換
  get query_tags_str() {
    return this.query_tags.map(tag => tag.name).join(' ')
  }

  // タグ選択フォームがクリックされた時
  onClickTagForm(e: MouseEvent) {
    e.preventDefault();
    (e.target as HTMLElement).blur()

    // ダイアログを開く
    const tagPicker = document.querySelector('#tagPickerQuery .modal')
    if (tagPicker) {
      let modal = new bootstrap.Modal(tagPicker)
      modal.show()
    }
  }

  onClickAdd(e: MouseEvent) {
    this.newNote = Note.empty()
    const editor = document.querySelector('#editorCreate .modal')
    if (editor) {
      let modal = new bootstrap.Modal(editor)
      modal.show()
    }
  }

  onEditNote(note: Note) {
    this.editNote = note
    const editor = document.querySelector('#editorUpdate .modal')
    if (editor) {
      let modal = new bootstrap.Modal(editor)
      modal.show()
    }
  }

  mounted(): void {
    dao.getNotes()
      .then(notes => this.notes = notes)
      .catch(err => {
        // 開発環境の場合は、ダミーデータを表示
        if (process.env.NODE_ENV == 'development') {
          this.notes = dummyNotes.slice()
        }
      })
  }
}

</script>

<style>
#sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;

  background-color: #ff9999;
}
#contents {
  background-color: #9999ff;
}
</style>
