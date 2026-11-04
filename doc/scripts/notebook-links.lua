-- Hide native Quarto notebook links when the current page hides answers.
-- The links themselves remain page-level `other-links`, so Quarto renders them
-- in its standard position below the page table of contents.

local function metadata_is_true(value)
  return value ~= nil and pandoc.utils.stringify(value) == "true"
end

local function add_to_header(meta, html)
  local includes = meta["header-includes"] or pandoc.MetaList({})
  table.insert(
    includes,
    pandoc.MetaBlocks({
      pandoc.RawBlock("html", html),
    })
  )
  meta["header-includes"] = includes
end

function Meta(meta)
  if metadata_is_true(meta["answers"]) then
    add_to_header(meta, [[
<script>
document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll('.quarto-other-links a[href$=".ipynb"]')
    .forEach((link) => link.setAttribute("download", ""));
});
</script>
]])
  else
    add_to_header(
      meta,
      "<style>.quarto-other-links { display: none !important; }</style>"
    )
  end

  return meta
end
