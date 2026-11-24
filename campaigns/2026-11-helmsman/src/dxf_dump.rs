use helmsman_drawing::*;
pub fn library() -> Vec<LibraryRecord> {
    let r = |id: &str, vendor: &str, model: &str, products: &[&str]| LibraryRecord {
        id: id.into(),
        vendor: vendor.into(),
        model: model.into(),
        products: products.iter().map(|s| (*s).into()).collect(),
    };
    vec![
        r("moxa/iologik-e1210", "Moxa", "ioLogik E1210", &[]),
        r("moxa/iologik-e1212", "Moxa", "ioLogik E1212", &[]),
        r("moxa/iologik-e1213", "Moxa", "ioLogik E1213", &[]),
        r(
            "murrelektronik/impact67-e-di16",
            "Murrelektronik",
            "IMPACT67 E DI16",
            &[],
        ),
        r(
            "murrelektronik/impact67-e-di8-do8",
            "Murrelektronik",
            "IMPACT67 E DI8 DO8",
            &[],
        ),
        r(
            "murrelektronik/impact67-e-dio8-dio8",
            "Murrelektronik",
            "IMPACT67 E DIO8 (DIO8)",
            &[],
        ),
        r(
            "ifm/if6123",
            "ifm",
            "IF6123, IF6124, IG6615, IG6616, II5973, II5974, IM5172, IM5173",
            &[
                "IF6123", "IF6124", "IG6615", "IG6616", "II5973", "II5974", "IM5172", "IM5173",
            ],
        ),
        r("ifm/kq6005", "ifm", "KQxxxx", &[]),
        r(
            "ifm/o5d100",
            "ifm",
            "O5D100/O5D102/O5D150/O5D152/O5D159",
            &["O5D100", "O5D102"],
        ),
        r(
            "ifm/pn7092",
            "ifm",
            "(PN7072, PN7092, PN7572, PN7592) Status B",
            &["PN7092"],
        ),
        r("sick/wtb4f-did8389194", "SICK", "WTB4F_DID8389194", &[]),
    ]
}
fn esc(s:&str)->String{s.replace('\\',"\\\\").replace('"',"\\\"")}
fn main(){
  let bytes=std::fs::read(std::env::args().nth(1).unwrap()).unwrap();
  let d=read(&bytes).unwrap();
  let p=parts(&d);
  let lib=library();
  let m=Matcher::new(&lib);
  println!("[");
  for (i,x) in p.parts.iter().enumerate(){
    let (kind,ids)=match m.match_part(x){Match::Matched(r)=>("matched",vec![r.id.clone()]),Match::Ambiguous(v)=>("ambiguous",v.iter().map(|r|r.id.clone()).collect()),Match::Unknown=>("unknown",vec![])};
    let near:Vec<String>=x.nearby_text.iter().map(|t|format!("\"{}\"",esc(&t.text))).collect();
    println!("{{\"block\":\"{}\",\"tag\":{},\"x\":{},\"y\":{},\"rot\":{},\"pn\":{},\"model\":{},\"near\":[{}],\"inside\":{:?},\"match\":\"{}\",\"ids\":{:?}}}{}",
      esc(&x.block), x.tag.as_ref().map(|t|format!("\"{}\"",esc(t))).unwrap_or("null".into()), x.x,x.y,x.rotation,
      x.part_number.as_ref().map(|t|format!("\"{}\"",esc(t))).unwrap_or("null".into()),
      x.model.as_ref().map(|t|format!("\"{}\"",esc(t))).unwrap_or("null".into()), near.join(","), x.inside, kind, ids, if i+1<p.parts.len(){","}else{""});
  }
  println!("]");
}
