/* *****************************************************************************
 * A.L.E (Arcade Learning Environment)
 * Copyright (c) 2009-2013 by Yavar Naddaf, Joel Veness, Marc G. Bellemare and
 *   the Reinforcement Learning and Artificial Intelligence Laboratory
 * Released under the GNU General Public License; see License.txt for details.
 *
 * Based on: Stella  --  "An Atari 2600 VCS Emulator"
 * Copyright (c) 1995-2007 by Bradford W. Mott and the Stella team
 *
 * *****************************************************************************
 *
 * RomSettings.cpp
 *
 * The interface to describe games as RL environments. It provides terminal and
 *  reward information.
 * *****************************************************************************
 */

#include "RomSettings2P.hpp"

#include <algorithm>
#include <unordered_set>

namespace ale {

RomSettings2P::RomSettings2P() {}

int RomSettings2P::livesP2() {
  return 0;
}

ModeVect RomSettings2P::oppositeModes(int num_modes) {
  ModeVect single_p_ms = getAvailableModes();
  std::unordered_set<int> single_p_modes(single_p_ms.begin(),single_p_ms.end());
  ModeVect other_modes;
  for(int mode = 0; mode < num_modes; mode++){
    if(!single_p_modes.count(mode)){
      other_modes.push_back(mode);
    }
  }
  return other_modes;
}
// bool RomSettings2P::in_two_player_list(int mode){
//   auto modes = get2PlayerModes();
//   return std::find(modes.begin(), modes.end(), m) != modes.end();
// }

}  // namespace ale
