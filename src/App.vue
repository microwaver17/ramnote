<template>
  <div>
    <!-- サイドバー・検索 -->
    <div class="row">
      <div id="sidebar" class="col-3 col-xl-3 col-xxl-2">
        <h2>RAMNOTE</h2>

        <button class="form-control" @click="showEditorCreate">Add</button>

        <label class="form-label">Keyword</label>
        <input class="form-control" type="text" :value="keyword" />
        <button class="form-control">Search</button>

        <label class="form-label">Tags</label>
        <input
          id="formTags"
          class="form-control"
          type="text"
          readonly
          :value="query_tags_str"
          @click="openTagPicker"
        />

        <label class="form-label">From</label>
        <input class="form-control" type="date" />

        <label class="form-label">To</label>
        <input class="form-control" type="date" />
      </div>

      <!-- メインカラム -->
      <div id="contents" class="col-9 col-xl-9 col-xxl-10 ms-auto">
        <!-- アラート -->
        <div class="alert alert-success" v-show="successMsg">
          {{ successMsg }}
        </div>
        <div class="alert alert-danger" v-show="errorMsg">
          {{ errorMsg }}
        </div>

        <!-- ノート一覧画面 -->
        <div v-if="currentTab == tabname.notelist">
          <div class="row justify-content-center">
            <NoteCard
              class="col-5 col-xl-4 col-xxl-2 m-2"
              v-for="note in notes"
              :key="note.id"
              :note="note"
              @edit="showEditPage"
              @delete="comfirmDeleteNote"
            ></NoteCard>
          </div>
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
        @close="isOpenTagPicker = false"
      ></TagPicker>
    </div>

    <!-- 削除確認ダイアログ -->
    <div id="deleteDialog" class="modal" tabindex="-1">
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

  flashError(msg: string, time = 3) {
    this.errorMsg = msg
    setTimeout((() => this.errorMsg = ''), time * 1000)
  }
  flashSuccess(msg: string, time = 3) {
    this.successMsg = msg
    setTimeout((() => this.successMsg = ''), time * 1000)
  }

  // タグをスペースで結合した形式に変換
  get query_tags_str() {
    return this.query_tags.map(tag => tag.name).join(' ')
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
    dao.getNotes()
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
    if (!this.editNote.id) {  // id が null の時は新規作成
      dao.createNote(this.editNote)
        .then(res => {
          this.fetchNotes()
          this.currentTab = this.tabname.notelist
          this.flashSuccess('追加しました')
        }).catch(err => {
          this.flashSuccess('失敗しました\n' + err.result)
        })
    }
  }

  commitUpdate() {
    if (this.editNote.id) {
      dao.updateNote(this.editNote)
        .then(res => {
          this.fetchNotes()
          this.currentTab = this.tabname.notelist
          this.flashSuccess('更新しました')
        }).catch(err => {
          this.flashSuccess('失敗しました\n' + err.result)
        })
    }
    this.flashSuccess('追加しました')
  }

  mounted() {
    this.fetchNotes()
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
