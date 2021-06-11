<template>
  <div>
    <!-- サイドバー・検索 -->
    <div>
      <div class="sidebar">
        <div class="mt-1 mb-3">
          <!-- ロゴ RAMNOTE -->
          <img
            src="@/assets/ramnote.svg"
            class="img-fluid pointer-cursor"
            style="cursor: pointer"
            @click="showInitialPage"
          />
        </div>

        <div class="mb-3 pb-3 border-bottom">
          <div class="mb-3">
            <label class="form-label">キーワード</label>
            <input
              type="search"
              class="form-control"
              style="-webkit-appearance: searchfield-cancel-button"
              v-model="keyword"
              @keydown="keydownAtKeywordInput"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">タグ</label>
            <input
              id="formTags"
              class="form-control"
              type="text"
              placeholder="クリックで追加"
              readonly
              :value="query_tags_str"
              @click="openTagPicker"
            />
          </div>

          <button class="btn btn-light form-control" @click="fetchNotes">
            検索
          </button>
        </div>

        <div class="mb-3">
          <button class="btn btn-light form-control" @click="showEditorCreate">
            メモを追加
          </button>
        </div>

        <div class="mb-3">
          <a :href="csvUrl" class="btn btn-light form-control">
            CSVエクスポート
          </a>
        </div>

        <!--
          実装予定の日時検索
        <label class="form-label">From</label>
        <input class="form-control" type="date" />

        <label class="form-label">To</label>
        <input class="form-control" type="date" />
        -->
      </div>

      <!-- メインカラム -->
      <div class="contents">
        <!-- アラート -->
        <div class="alert alert-success" v-show="successMsg">
          {{ successMsg }}
        </div>
        <div class="alert alert-danger" v-show="errorMsg">
          {{ errorMsg }}
        </div>

        <!-- ノート一覧画面 -->
        <div class="d-flex flex-wrap" v-if="currentTab == tabname.notelist">
          <NoteCard
            class="m-1"
            v-for="note in notes"
            :key="note.id"
            :note="note"
            @edit="showEditPage"
            @delete="comfirmDeleteNote"
          ></NoteCard>
        </div>

        <!-- ノート作成画面 -->
        <div v-if="currentTab == tabname.editor">
          <NoteEditor
            :note="editNote"
            @cancel="currentTab = tabname.notelist"
            @create="commitCreate"
            @update="commitUpdate"
          ></NoteEditor>
        </div>
      </div>
    </div>

    <!-- 検索用タグ選択画面 -->
    <div id="tagPickerQuery">
      <TagPicker
        :tags="query_tags"
        :visible="isOpenTagPicker"
        @close="tagPickerClosed"
      ></TagPicker>
    </div>

    <!-- 削除確認ダイアログ -->
    <div id="deleteDialog" class="modal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
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
              @click="commitDelete"
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
import bootstrap from "bootstrap"

import NoteCard from "./components/NoteCard.vue"
import TagPicker from "./components/TagPicker.vue"
import NoteEditor from "./components/NoteEditor.vue"
import { Note, Tag } from "./models"
import { dao } from "./dao"
import { consts } from "./consts"
import { config } from './config'

@Options({
  components: {
    NoteCard,
    TagPicker,
    NoteEditor,
  },
})
export default class App extends Vue {
  readonly tabname = {
    notelist: 'notelist',
    editor: 'editor'
  }

  notes: Note[] = []  // 表示するノート
  editNote: Note = Note.empty()

  query_tags: Tag[] = []
  keyword = ''

  currentTab = this.tabname.notelist  // メインカラムに表示するもの
  successMsg = ''
  errorMsg = ''
  isOpenTagPicker = false

  // タグをスペースで結合した形式に変換
  get query_tags_str() {
    return this.query_tags.map(tag => tag.name).join(' ')
  }

  get csvUrl() {
    return config.apiRoot + 'export/csv'
  }

  flashError(msg: string, time = 3) {
    this.errorMsg = msg
    setTimeout((() => this.errorMsg = ''), time * 1000)
  }
  flashSuccess(msg: string, time = 3) {
    this.successMsg = msg
    setTimeout((() => this.successMsg = ''), time * 1000)
  }

  keydownAtKeywordInput(e: KeyboardEvent) {
    if (e.key == 'Enter') {
      this.fetchNotes()
    }
  }

  tagPickerClosed() {
    this.isOpenTagPicker = false
    this.fetchNotes()
  }

  showInitialPage() {
    this.keyword = ''
    this.query_tags = []
    this.fetchNotes()
    this.currentTab = this.tabname.notelist
  }

  // タグ選択フォームがクリックされた時
  openTagPicker(e: MouseEvent) {
    e.preventDefault();
    (e.target as HTMLElement).blur()
    this.isOpenTagPicker = true
  }

  showNoteList(e: MouseEvent) {
    this.currentTab = this.tabname.notelist
  }

  showEditorCreate(e: MouseEvent) {
    this.editNote = Note.empty()
    this.currentTab = this.tabname.editor
  }

  showEditPage(note: Note) {
    this.editNote = note.clone()
    this.currentTab = this.tabname.editor
  }

  comfirmDeleteNote(note: Note) {
    // 削除確認ダイアログを開く
    const dialog = document.querySelector('#deleteDialog')
    if (dialog) {
      this.editNote = note.clone()
      let modal = new bootstrap.Modal(dialog)
      modal.show()
    }
  }

  fetchNotes() {
    dao.getNotes(this.keyword, this.query_tags)
      .then(notes => this.notes = notes)
      .catch(err => {
        this.flashError(err.result)
        console.log(err)
        // 開発環境の場合は、ダミーデータを表示
        // if (process.env.NODE_ENV == 'development') {
        //   this.notes = consts.dummyNotes.slice()
        // }
      })
  }

  commitDelete() {
    if (this.editNote.id) {
      dao.deleteNote(this.editNote).then(res => {
        this.fetchNotes()
        this.flashSuccess('削除しました')
      }).catch(err => {
        this.flashSuccess('失敗しました\n' + err.result)
      })
    }
  }

  commitCreate() {
    if (this.editNote.id == null) {  // id が null の時は新規作成
      this.editNote.date = new Date() // 改めて現在日時を格納
      dao.createNote(this.editNote)
        .then(res => {
          this.fetchNotes()
          this.flashSuccess('追加しました')
          this.editNote = Note.empty()
        }).catch(err => {
          this.flashSuccess('失敗しました\n' + err.result)
        })
    }
  }

  commitUpdate() {
    if (this.editNote.id != null) {
      dao.updateNote(this.editNote)
        .then(res => {
          this.fetchNotes()
          this.flashSuccess('更新しました')
        }).catch(err => {
          this.flashSuccess('失敗しました\n' + err.result)
        })
    }
  }

  mounted() {
    this.fetchNotes()
  }
}

</script>

<style scoped>
button:focus,
.btn:focus {
  outline: none !important;
  box-shadow: none !important;
}
.sidebar {
  z-index: 100;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 200px;
  padding: 10px;

  color: #ffffff;
  background-color: #313131;
}
.contents {
  z-index: 100;
  position: fixed;
  top: 0;
  left: 200px;
  right: 0;
  bottom: 0;
  padding: 10px;

  background-color: #fafafa;
}
.alert {
  z-index: 10000;
  position: fixed;
  bottom: 0;
  left: 200px;
  right: 0;
  margin: 10px;
}
</style>
