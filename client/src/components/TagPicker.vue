<!-- タグ選択ダイアログ -->
<template>
  <div v-show="visible">
    <div class="modal" style="display: block" tabindex="-1">
      <div
        class="
          modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg
        "
        style="max-width: 500px"
      >
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">タグ選択</h5>
          </div>

          <div class="modal-body">
            <div class="container-fluid">
              <div class="row">
                <div id="tagpicker_taglist" class="col-8 overflow-scroll">
                  <!-- 登録済みタグ一覧 -->
                  <div class="list-group" style="height: 50vh">
                    <button
                      style="outline: none"
                      v-for="tag in tagFiltered"
                      :key="tag.id"
                      @click="addTag(tag)"
                      class="list-group-item list-group-item-action pt-1 pb-1"
                    >
                      <div class="d-flex">
                        <div>
                          {{ tag.name }}
                        </div>
                        <div class="ms-auto">{{ tag.used_count }}件</div>
                      </div>
                    </button>
                  </div>
                </div>

                <div class="col-4">
                  <div class="mb-4">
                    <label class="form-label">絞り込み</label>
                    <input
                      type="search"
                      class="form-control"
                      style="-webkit-appearance: searchfield-cancel-button"
                      v-model="tagFilterKeyword"
                    />
                  </div>
                  <div class="mb-2">
                    <label class="form-label">タグ追加</label>
                    <input
                      type="text"
                      class="form-control mb-2"
                      v-model="newTag"
                    />
                    <button class="form-control btn-primary" @click="createTag">
                      追加
                    </button>
                  </div>
                </div>
              </div>

              <div
                class="
                  row
                  border-top border-top border-bottom
                  mt-3
                  mb-3
                  pt-2
                  pb-2
                  mw-100
                "
              >
                <div class="col-12">
                  <span
                    v-if="tags.length == 0"
                    class="border rounded bg-primary text-white p-2 float-start"
                    style="opacity: 0"
                  >
                    ダミー
                  </span>
                  <span
                    v-for="tag in tags"
                    :key="tag.id"
                    class="border rounded bg-primary text-white p-2 float-start"
                    >{{ tag.name }}
                    <button
                      class="btn-close btn-close-white"
                      style="font-size: 0.7em"
                      @click="removeTag(tag)"
                    ></button>
                  </span>
                </div>
              </div>
            </div>
            <div class="d-flex">
              <button class="btn btn-primary ms-auto" @click="close">OK</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-backdrop show"></div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { dao } from "../dao";
import { Tag } from "../models";

@Options({
  props: {
    tags: {
      type: Array,
      default: [],
    },
    visible: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    visible() {
      this.changeVisibility();
    },
  },
})
export default class TagPicker extends Vue {
  tags!: Tag[]; // 選択中のタグ一覧
  visible!: boolean;

  availableTags: Tag[] = [];
  tagFilterKeyword = "";
  newTag = "";

  get tagFiltered(): Tag[] {
    return this.availableTags.filter((tag) =>
      tag.name.toLowerCase().includes(this.tagFilterKeyword.toLowerCase())
    );
  }

  close(): void {
    this.$emit("close");
  }

  changeVisibility(): void {
    if (this.visible) {
      this.tagFilterKeyword = "";
      this.newTag = "";
      // 表示時にタグ一覧を取得
      dao.getTags().then((tags) => {
        this.availableTags = tags;
        // タグ一覧を一番上にスクロール
        // idかぶりで動かない
        // const taglist = document.getElementById('tagpicker_taglist')
        // if (taglist) {
        //   taglist.scrollTop = 0
        // }
      });
    }
  }

  // タグを追加する
  addTag(tag: Tag): void {
    const match_tag = this.tags.filter((_tag) => _tag.id == tag.id);
    if (match_tag.length == 0) {
      this.tags.push(tag);
      this.tagFilterKeyword = "";
    }
  }

  // タグを選択から削除する
  removeTag(tag: Tag): void {
    let idx = this.tags.indexOf(tag);
    this.tags.splice(idx, 1);
  }

  createTag(): void {
    const tagname = this.newTag;
    const tag = new Tag(null, tagname, -1);
    // タグをDBに登録後、タグ一覧をリクエストして、id を取得する
    // その後、新しく登録したタグを選択状態にする
    dao
      .createTag(tag)
      .then((res) =>
        dao
          .getTags()
          .then((tags) => {
            const tag = tags.find((tag) => tag.name == tagname);
            if (tag) {
              this.addTag(tag);
              this.availableTags = tags;
              this.newTag = "";
            } else {
              console.error("タグ登録失敗");
            }
          })
          .catch((err) => console.error(err.result))
      )
      .catch((err) => console.error(err.result));
  }
}
</script>

<style scoped></style>
