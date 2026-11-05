-- Keep defaults here so shared metadata does not override local course choices.
function Meta(meta)
  if not quarto.doc.is_format("revealjs") then return meta end
  local enabled = meta["repeated-slide-titles"] == nil
    or pandoc.utils.stringify(meta["repeated-slide-titles"]) ~= "false"
  local payload = quarto.json.encode({repeatedSlideTitles = enabled})
  quarto.doc.include_text("in-header",
    "<script>window.courseSlideOptions = " .. payload .. ";</script>")
  return meta
end
