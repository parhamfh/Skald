import java.io.*;
import java.util.*;
import javax.sound.midi.*;

public class TestMidi {

	public TestMidi() throws Exception {
		Sequence seq = MidiSystem.getSequence(new File("midi/frm.mid"));
		int t = 0;
		HashMap<Long,String> lyrics = new HashMap<Long,String>();
		HashMap<Long,Integer> notes = new HashMap<Long,Integer>();
		HashMap<Long,Integer> tracks = new HashMap<Long,Integer>();
		List<String> lines = new ArrayList<String>();
		
		System.out.println(seq.getTracks().length);
		for (Track track : seq.getTracks()) {
			if (t == 9 || t == 3 || t == 4 || t == 2 || t == 0) {
				System.out.println("TRACK "+t+"("+track.size()+")");
				for (int i = 0; i < track.size(); i++) {
					long tick = track.get(i).getTick();
					String stick = String.format("%05d", tick);
					MidiMessage mess = track.get(i).getMessage();
					if (mess instanceof MetaMessage) {
						MetaMessage meta = (MetaMessage)mess;
						lines.add(stick + " " + t + " " + new String(meta.getData()));
						if (tick > 0)
							lyrics.put(tick, new String(meta.getData()));
					} else if (mess instanceof ShortMessage) {
						ShortMessage smess = (ShortMessage)mess;
						if (smess.getCommand() == 144 && smess.getData2() != 0) {
							notes.put(tick, smess.getData1());
							tracks.put(tick, smess.getChannel());
						}
						lines.add(stick + " " + t + " " + smess.getCommand() + "/" + smess.getData1() + "/" + smess.getData2() + " ");
					}
				}
			}
			t++;
		}
		List<Long> times = new ArrayList<Long>(lyrics.keySet());
		Collections.sort(times);
		for (Long time : times) {
			String word = lyrics.get(time);
			if (word.length() != 0) {
				if (!word.startsWith(" ") && !word.startsWith("\\") && !word.startsWith("/"))
					word = "-" + word;
				word = word.trim();
				System.out.println(time + "\t" + word + "\t" + notes.get(time) + "\t" + tracks.get(time));
			}
		}
	}
	
	public static void main(String[] args) throws Exception {
		new TestMidi();
	}
	
}
