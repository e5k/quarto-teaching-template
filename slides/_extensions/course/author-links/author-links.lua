-- Personal URLs belong in _quarto.yml; this filter can be shared unchanged.
function Meta(meta)
  if not quarto.doc.is_format("revealjs") or not meta["author-links"] then
    return meta
  end
  local links = {}
  for _, item in ipairs({
    {"researchgate", "ResearchGate", "fa-brands fa-researchgate"},
    {"github", "GitHub", "fa-brands fa-github"},
    {"scholar", "Google Scholar", "fa-solid fa-graduation-cap"},
    {"website", "Website", "fa-solid fa-globe"}
  }) do
    local value = meta["author-links"][item[1]]
    if value then
      local url = pandoc.utils.stringify(value)
      if url:match("^https?://") then
        table.insert(links, {url = url, label = item[2], icon = item[3]})
      end
    end
  end
  if #links == 0 then return meta end
  local payload = quarto.json.encode(links):gsub("<", "\\u003c")
  quarto.doc.include_text("after-body", [[
<style>
.reveal .quarto-title-author-name a.author-profile-link,
.reveal .quarto-title-author-name a.quarto-title-author-orcid {
  color: #2F4647; opacity: .55;
  transition: opacity .15s ease;
}
.reveal .quarto-title-author-name a.author-profile-link:hover,
.reveal .quarto-title-author-name a.author-profile-link:focus-visible,
.reveal .quarto-title-author-name a.quarto-title-author-orcid:hover,
.reveal .quarto-title-author-name a.quarto-title-author-orcid:focus-visible {
  color: #2F4647; opacity: 1;
}
.quarto-title-author-name .quarto-title-author-orcid {
  font-size: 16px; vertical-align: middle; line-height: 1;
}
.quarto-title-author-name .author-profile-link {
  display: inline-block; margin-left: .3em; font-size: 16px;
  vertical-align: middle; line-height: 1; text-decoration: none;
}
</style>
<script>
(function () {
  function addAuthorLinks() {
    const author = document.querySelector('.quarto-title-author-name');
    if (!author || author.querySelector('.author-profile-link')) return;
    const links = ]] .. payload .. [[;
    let anchor = author.querySelector('.quarto-title-author-orcid');
    if (anchor) {
      anchor.title = 'ORCID';
      anchor.setAttribute('aria-label', 'ORCID');
      const icon = document.createElement('i');
      icon.className = 'fa-brands fa-orcid';
      icon.setAttribute('aria-hidden', 'true');
      anchor.replaceChildren(icon);
    }
    links.forEach(function (item) {
      const link = document.createElement('a');
      link.href = item.url;
      link.className = 'author-profile-link';
      link.title = item.label;
      link.setAttribute('aria-label', item.label);
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      const icon = document.createElement('i');
      icon.className = item.icon;
      icon.setAttribute('aria-hidden', 'true');
      link.appendChild(icon);
      if (anchor) anchor.after(link); else author.appendChild(link);
      anchor = link;
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addAuthorLinks);
  } else addAuthorLinks();
})();
</script>
]])
  return meta
end
