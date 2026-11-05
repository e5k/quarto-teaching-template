-- Personal URLs and visibility choices belong in local YAML, not this filter.
local function is_false(value)
  return value == false
end

function Meta(meta)
  local config = meta["author-links"]
  if not quarto.doc.is_format("revealjs") or config == nil or is_false(config) then
    return meta
  end
  -- A map is required; bare true does not provide any profile URLs.
  if type(config) ~= "table" then return meta end

  local services = {
    researchgate = {label = "ResearchGate", icon = "fa-brands fa-researchgate"},
    github = {label = "GitHub", icon = "fa-brands fa-github"},
    scholar = {label = "Google Scholar", icon = "fa-solid fa-graduation-cap"},
    website = {label = "Website", icon = "fa-solid fa-globe"}
  }
  local order = config.order or {"researchgate", "github", "scholar", "website"}
  if pandoc.utils.type(order) == "Inlines" or type(order) == "string" then
    local text = pandoc.utils.stringify(order)
    order = {}
    for key in text:gmatch("[^,%s]+") do table.insert(order, key) end
  elseif type(order) ~= "table" then
    order = {"researchgate", "github", "scholar", "website"}
  end
  local links = {}
  local seen = {}
  if not is_false(config.enabled) then
    for _, name in ipairs(order) do
      local key = pandoc.utils.stringify(name)
      local service = services[key]
      local value = config[key]
      if service and not seen[key] and value ~= nil and not is_false(value) then
        seen[key] = true
        local enabled = true
        local url_value = value
        if type(value) == "table" and (value.url ~= nil or value.enabled ~= nil) then
          enabled = not is_false(value.enabled)
          url_value = value.url
        end
        if enabled and url_value ~= nil then
          local url = pandoc.utils.stringify(url_value)
          if url:match("^https?://") then
            table.insert(links, {url = url, label = service.label, icon = service.icon})
          end
        end
      end
    end
  end
  -- Preserve an array for the browser even when every optional icon is disabled.
  local payload = #links > 0 and quarto.json.encode(links):gsub("<", "\\u003c") or "[]"
  local show_orcid = not is_false(config.orcid)
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
    const showOrcid = ]] .. tostring(show_orcid) .. [[;
    let anchor = author.querySelector('.quarto-title-author-orcid');
    if (anchor && !showOrcid) {
      anchor.remove();
      anchor = null;
    }
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
